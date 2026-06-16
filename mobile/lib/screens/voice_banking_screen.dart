import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:vibration/vibration.dart';
import 'package:flutter_tts/flutter_tts.dart';
import '../services/api_service.dart';

enum SessionStep { idle, menu, balanceAccount, balanceResult, loanPurpose, loanAmount, loanConfirm, loanResult, branchLocation, branchResult }

class VoiceBankingScreen extends StatefulWidget {
  const VoiceBankingScreen({super.key});
  @override
  State<VoiceBankingScreen> createState() => _VoiceBankingScreenState();
}

class _VoiceBankingScreenState extends State<VoiceBankingScreen> {
  final _api = ApiService();
  final _tts = FlutterTts();
  final _textController = TextEditingController();
  final _scrollController = ScrollController();

  String _language = 'hi';
  String _sessionId = '';
  SessionStep _step = SessionStep.idle;
  bool _loading = false;
  String _error = '';

  double _loanAmount = 0;
  String _loanPurpose = '';

  final List<Map<String, String>> _messages = [];

  final _langLabels = {
    'hi': 'हिन्दी',
    'ta': 'தமிழ்',
    'en': 'English',
  };

  final _langCodes = ['hi', 'ta', 'en'];

  @override
  void initState() {
    super.initState();
    _initTts();
  }

  Future<void> _initTts() async {
    await _tts.setLanguage('hi-IN');
    await _tts.setSpeechRate(0.5);
    await _tts.setVolume(1.0);
  }

  Future<void> _speak(String text) async {
    final langMap = {'hi': 'hi-IN', 'ta': 'ta-IN', 'en': 'en-IN'};
    await _tts.setLanguage(langMap[_language] ?? 'hi-IN');
    await _tts.speak(text);
  }

  void _addMessage(String role, String text) {
    setState(() => _messages.add({'role': role, 'text': text}));
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _hapticSuccess() async {
    try {
      await Vibration.vibrate(duration: 100);
    } on PlatformException {
      // Haptic not available
    }
  }

  Future<void> _hapticError() async {
    try {
      await Vibration.vibrate(duration: 100);
      await Future.delayed(const Duration(milliseconds: 150));
      await Vibration.vibrate(duration: 100);
    } on PlatformException {
      // Haptic not available
    }
  }

  Future<void> _processText(String text) async {
    if (text.trim().isEmpty || _loading) return;
    _addMessage('user', text);
    setState(() => _loading = true);

    try {
      final res = await _api.processVoice(
        text: text.trim(),
        language: _language,
        sessionId: _sessionId.isNotEmpty ? _sessionId : null,
      );
      _sessionId = res['session_id'] ?? '';
      final responseText = res['response_text'] ?? '';
      _addMessage('system', responseText);
      await _speak(responseText);
      await _hapticSuccess();

      final intent = res['intent'] ?? '';
      setState(() {
        switch (intent) {
          case 'balance': _step = SessionStep.balanceAccount; break;
          case 'loan': _step = SessionStep.loanPurpose; break;
          case 'branch': _step = SessionStep.branchLocation; break;
          case 'goodbye': _step = SessionStep.idle; break;
          default: _step = SessionStep.menu;
        }
      });
    } catch (e) {
      setState(() => _error = e.toString());
      await _hapticError();
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _submitBalance(String account) async {
    setState(() => _loading = true);
    try {
      _addMessage('user', 'खाता: $account');
      final res = await _api.checkBalance(accountNumber: account, language: _language);
      _addMessage('system', res['response_text'] ?? '');
      await _speak(res['response_text'] ?? '');
      await _hapticSuccess();
      setState(() => _step = SessionStep.balanceResult);
    } catch (e) {
      setState(() => _error = e.toString());
      await _hapticError();
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _submitLoanPurpose(String purpose) async {
    _loanPurpose = purpose;
    _addMessage('user', purpose);
    final prompt = {
      'hi': 'कृपया लोन राशि बताएं।',
      'ta': 'கடன் தொகையைக் கூறுங்கள்।',
      'en': 'Please state the loan amount.',
    }[_language]!;
    _addMessage('system', prompt);
    await _speak(prompt);
    setState(() => _step = SessionStep.loanAmount);
  }

  Future<void> _submitLoanAmount(String amountStr) async {
    final amount = double.tryParse(amountStr.replaceAll(RegExp(r'[^0-9.]'), ''));
    if (amount == null || amount <= 0) {
      final errMsg = {'hi': 'सही राशि दर्ज करें', 'ta': 'சரியான தொகையை உள்ளிடவும்', 'en': 'Enter valid amount'}[_language]!;
      setState(() => _error = errMsg);
      await _hapticError();
      return;
    }
    _loanAmount = amount;
    _addMessage('user', '₹$amount');
    final confirmText = {
      'hi': 'क्या आप ₹$amount का लोन $_loanPurpose के लिए आवेदन करना चाहते हैं? हां के लिए 1, रद्द के लिए 2 दबाएं।',
      'ta': 'நீங்கள் ₹$amount கடனை $_loanPurposeக்காக விண்ணப்பிக்க விரும்புகிறீர்களா? ஆம் எனில் 1, ரத்து செய்ய 2 அழுத்தவும்.',
      'en': 'Do you want to apply for a loan of ₹$amount for $_loanPurpose? Press 1 for yes, 2 to cancel.',
    }[_language]!;
    _addMessage('system', confirmText);
    await _speak(confirmText);
    setState(() => _step = SessionStep.loanConfirm);
  }

  Future<void> _confirmLoan(bool confirm) async {
    if (!confirm) {
      final cancelText = {'hi': 'लोन आवेदन रद्द।', 'ta': 'கடன் விண்ணப்பம் ரத்து.', 'en': 'Loan cancelled.'}[_language]!;
      _addMessage('system', cancelText);
      await _speak(cancelText);
      setState(() => _step = SessionStep.idle);
      return;
    }
    setState(() => _loading = true);
    try {
      final res = await _api.applyLoan(amount: _loanAmount, purpose: _loanPurpose, language: _language);
      _addMessage('system', res['response_text'] ?? '');
      await _speak(res['response_text'] ?? '');
      await _hapticSuccess();
      setState(() => _step = SessionStep.loanResult);
    } catch (e) {
      setState(() => _error = e.toString());
      await _hapticError();
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _submitBranch(String location) async {
    setState(() => _loading = true);
    try {
      _addMessage('user', location);
      final res = await _api.findBranch(location: location, language: _language);
      _addMessage('system', res['response_text'] ?? '');
      await _speak(res['response_text'] ?? '');
      await _hapticSuccess();
      setState(() => _step = SessionStep.branchResult);
    } catch (e) {
      setState(() => _error = e.toString());
      await _hapticError();
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text('OSAM Voice Banking', style: TextStyle(color: Color(0xFFF1F5F9), fontWeight: FontWeight.bold)),
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.language, color: Color(0xFF94A3B8)),
            onSelected: (code) => setState(() => _language = code),
            itemBuilder: (_) => _langCodes.map((code) => PopupMenuItem(
              value: code,
              child: Text(_langLabels[code] ?? code),
            )).toList(),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(32),
                    child: Text(
                      'नमस्कार! मैं OSAM हूँ।\nबोलें: "बैलेंस चेक", "लोन", या "शाखा खोजें"',
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Color(0xFF94A3B8), fontSize: 16),
                    ),
                  ),
                )
              : ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.all(16),
                  itemCount: _messages.length,
                  itemBuilder: (_, i) {
                    final msg = _messages[i];
                    final isUser = msg['role'] == 'user';
                    return Align(
                      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                      child: Container(
                        margin: const EdgeInsets.only(bottom: 8),
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        decoration: BoxDecoration(
                          color: isUser ? const Color(0xFF6366F1) : const Color(0xFF1E293B),
                          borderRadius: BorderRadius.only(
                            topLeft: const Radius.circular(18),
                            topRight: const Radius.circular(18),
                            bottomLeft: isUser ? const Radius.circular(18) : const Radius.circular(4),
                            bottomRight: isUser ? const Radius.circular(4) : const Radius.circular(18),
                          ),
                          border: isUser ? null : Border.all(color: const Color(0x276366F1)),
                        ),
                        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
                        child: Text(
                          msg['text'] ?? '',
                          style: TextStyle(
                            color: isUser ? Colors.white : const Color(0xFFF1F5F9),
                            fontSize: 15,
                          ),
                        ),
                      ),
                    );
                  },
                ),
          ),
          if (_loading)
            const Padding(
              padding: EdgeInsets.all(8),
              child: CircularProgressIndicator(color: Color(0xFF6366F1), strokeWidth: 2),
            ),
          if (_error.isNotEmpty)
            Padding(
              padding: const EdgeInsets.all(8),
              child: Text('⚠️ $_error', style: const TextStyle(color: Color(0xFFEF4444), fontSize: 13)),
            ),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: const BoxDecoration(
              color: Color(0xFF1E293B),
              border: Border(top: BorderSide(color: Color(0x276366F1))),
            ),
            child: Column(
              children: [
                Row(
                  children: [
                    Expanded(
                      child: TextField(
                        controller: _textController,
                        enabled: !_loading,
                        style: const TextStyle(color: Color(0xFFF1F5F9)),
                        decoration: InputDecoration(
                          hintText: {'hi': 'यहाँ टाइप करें...', 'ta': 'இங்கே தட்டச்சு செய்க...', 'en': 'Type here...'}[_language],
                          hintStyle: const TextStyle(color: Color(0xFF64748B)),
                          filled: true,
                          fillColor: const Color(0xFF0F172A),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(24),
                            borderSide: const BorderSide(color: Color(0x276366F1)),
                          ),
                          contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                        ),
                        onSubmitted: (text) {
                          _textController.clear();
                          _processText(text);
                        },
                      ),
                    ),
                    const SizedBox(width: 8),
                    Semantics(
                      label: 'भेजें',
                      child: IconButton(
                        icon: const Icon(Icons.send_rounded, color: Color(0xFF6366F1)),
                        onPressed: _loading || _textController.text.trim().isEmpty ? null : () {
                          final text = _textController.text;
                          _textController.clear();
                          _processText(text);
                        },
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      _chip('💰 बैलेंस', () => _processText('मेरा बैलेंस चेक करें')),
                      _chip('📋 लोन', () => _processText('लोन के लिए आवेदन करें')),
                      _chip('📍 शाखा', () => _processText('निकटतम शाखा खोजें')),
                      _chip('🔄 रीसेट', () {
                        setState(() {
                          _step = SessionStep.idle;
                          _sessionId = '';
                          _messages.clear();
                          _error = '';
                          _loanAmount = 0;
                          _loanPurpose = '';
                        });
                      }),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _chip(String label, VoidCallback onTap) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: Semantics(
        label: label,
        child: ActionChip(
          label: Text(label, style: const TextStyle(fontSize: 12, color: Color(0xFF94A3B8))),
          backgroundColor: Colors.transparent,
          side: const BorderSide(color: Color(0x276366F1)),
          onPressed: _loading ? null : onTap,
        ),
      ),
    );
  }

  @override
  void dispose() {
    _textController.dispose();
    _scrollController.dispose();
    _tts.stop();
    super.dispose();
  }
}
