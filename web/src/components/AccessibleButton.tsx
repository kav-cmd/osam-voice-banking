import React from 'react';

export default function AccessibleButton({
  onClick,
  label,
  description,
  variant = 'primary',
  disabled = false,
  lang,
}: {
  onClick: () => void;
  label: string;
  description?: string;
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  disabled?: boolean;
  lang?: string;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      aria-label={description || label}
      lang={lang}
      className={`a11y-btn btn-${variant}`}
      tabIndex={0}
    >
      {label}
    </button>
  );
}
