import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ApiService {
  static const String _baseUrl = String.fromEnvironment(
    'API_BASE',
    defaultValue: 'http://10.0.2.2:8002',
  );

  Future<Map<String, dynamic>> processVoice({
    String? text,
    String language = 'hi',
    String? sessionId,
  }) async {
    final res = await http.post(
      Uri.parse('$_baseUrl/api/voice/process'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'text': text,
        'language': language,
        'session_id': sessionId,
      }),
    );
    if (res.statusCode != 200) throw Exception('Voice processing failed');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> checkBalance({
    required String accountNumber,
    String language = 'hi',
  }) async {
    final res = await http.post(
      Uri.parse('$_baseUrl/api/balance'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'account_number': accountNumber,
        'language': language,
      }),
    );
    if (res.statusCode != 200) throw Exception('Balance check failed');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> applyLoan({
    required double amount,
    required String purpose,
    String language = 'hi',
  }) async {
    final res = await http.post(
      Uri.parse('$_baseUrl/api/loan/apply'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'amount': amount,
        'purpose': purpose,
        'language': language,
      }),
    );
    if (res.statusCode != 200) throw Exception('Loan application failed');
    return jsonDecode(res.body);
  }

  Future<Map<String, dynamic>> findBranch({
    required String location,
    String language = 'hi',
  }) async {
    final res = await http.post(
      Uri.parse('$_baseUrl/api/branch/nearby'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'location': location,
        'language': language,
      }),
    );
    if (res.statusCode != 200) throw Exception('Branch lookup failed');
    return jsonDecode(res.body);
  }

  Future<List<Map<String, dynamic>>> getLanguages() async {
    final res = await http.get(Uri.parse('$_baseUrl/api/languages'));
    if (res.statusCode != 200) throw Exception('Failed to load languages');
    return List<Map<String, dynamic>>.from(jsonDecode(res.body)['languages']);
  }

  Future<Map<String, dynamic>> uploadAudio(
    File audioFile, {
    String language = 'hi',
  }) async {
    final req = http.MultipartRequest(
      'POST',
      Uri.parse('$_baseUrl/api/voice/upload'),
    );
    req.fields['language'] = language;
    req.files.add(await http.MultipartFile.fromPath('file', audioFile.path));
    final streamedRes = await req.send();
    final res = await http.Response.fromStream(streamedRes);
    if (res.statusCode != 200) throw Exception('Audio upload failed');
    return jsonDecode(res.body);
  }
}
