import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '../../api/auth';
import { useAuth } from '../../app/providers';

type PinStatus = 'idle' | 'verifying' | 'success' | 'error' | 'locked';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [pin, setPin] = useState('');
  const [status, setStatus] = useState<PinStatus>('idle');
  const [errorMsg, setErrorMsg] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-focus on mount
  useEffect(() => {
    const t = setTimeout(() => inputRef.current?.focus(), 100);
    return () => clearTimeout(t);
  }, []);

  const mutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: (response) => {
      setStatus('success');
      login(response.data.token);
      navigate('/');
    },
    onError: (error: any) => {
      const msg = error.message || '';
      setPin('');
      if (msg.toLowerCase().includes('lock') || msg.toLowerCase().includes('temporarily')) {
        setStatus('locked');
        setErrorMsg(msg);
      } else {
        setStatus('error');
        setErrorMsg('Incorrect PIN');
      }
      // Re-focus so user can try again
      setTimeout(() => inputRef.current?.focus(), 80);
    },
  });

  const handlePinChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const digits = e.target.value.replace(/\D/g, '').slice(0, 4);
    setPin(digits);

    // Reset error when user starts typing again
    if (status === 'error' || status === 'locked') {
      setStatus('idle');
      setErrorMsg('');
    }

    // Auto-submit when 4 digits entered
    if (digits.length === 4) {
      setStatus('verifying');
      mutation.mutate({ pin: digits });
    }
  };

  const isDisabled = status === 'verifying' || status === 'locked' || status === 'success';

  const dotColor = (filled: boolean): string => {
    if (!filled) return 'bg-slate-200 dark:bg-slate-600';
    switch (status) {
      case 'success':  return 'bg-green-500 scale-110';
      case 'error':    return 'bg-red-400 scale-110 animate-bounce';
      case 'locked':   return 'bg-orange-400 scale-110';
      case 'verifying': return 'bg-blue-400 animate-pulse';
      default:          return 'bg-slate-800 dark:bg-white scale-110';
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 px-4">
      <div className="w-full max-w-sm">

        {/* Branding */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-slate-900 dark:bg-white mb-4 shadow-lg">
            <span className="text-white dark:text-slate-900 text-xl font-black tracking-tighter">A</span>
          </div>
          <h1 className="text-2xl font-black tracking-widest text-slate-900 dark:text-white uppercase">ARTHA</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Secure Billing Platform</p>
        </div>

        {/* Card */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-700 p-8">
          <div className="text-center mb-8">
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Enter your PIN</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">4-digit secure access code</p>
          </div>

          {/* PIN dot indicators */}
          <div className="flex justify-center gap-4 mb-4">
            {[0, 1, 2, 3].map((i) => (
              <div
                key={i}
                className={`w-4 h-4 rounded-full transition-all duration-150 ${dotColor(i < pin.length)}`}
              />
            ))}
          </div>

          {/* Hidden input — captures actual typing */}
          <input
            ref={inputRef}
            type="password"
            inputMode="numeric"
            pattern="[0-9]*"
            autoComplete="one-time-code"
            maxLength={4}
            value={pin}
            onChange={handlePinChange}
            disabled={isDisabled}
            className="sr-only"
            aria-label="Enter 4-digit PIN"
          />

          {/* Tap-target / status line */}
          <button
            type="button"
            onClick={() => !isDisabled && inputRef.current?.focus()}
            disabled={isDisabled}
            className={`w-full mt-2 py-3 rounded-xl border-2 text-sm transition-all duration-200 focus:outline-none ${
              status === 'idle' || status === 'verifying'
                ? 'border-dashed border-slate-200 dark:border-slate-600 text-slate-400 dark:text-slate-500 hover:border-slate-400 dark:hover:border-slate-400 cursor-text'
                : 'border-transparent'
            }`}
          >
            {status === 'idle' && pin.length === 0 && (
              <span>Tap here, then type your PIN</span>
            )}
            {status === 'idle' && pin.length > 0 && pin.length < 4 && (
              <span className="text-slate-500">{pin.length} of 4 digits entered…</span>
            )}
            {status === 'verifying' && (
              <span className="text-blue-500 font-medium">Verifying…</span>
            )}
            {status === 'success' && (
              <span className="text-green-600 dark:text-green-400 font-semibold">✓ PIN verified — redirecting…</span>
            )}
            {status === 'error' && (
              <span className="text-red-500 font-semibold">✕ {errorMsg}</span>
            )}
            {status === 'locked' && (
              <span className="text-orange-500 font-semibold">⚠ Account locked</span>
            )}
          </button>

          {/* Expanded error/locked message */}
          {(status === 'error' || status === 'locked') && (
            <div
              className={`mt-4 p-3 rounded-lg text-sm text-center ${
                status === 'locked'
                  ? 'bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-400 border border-orange-100 dark:border-orange-800'
                  : 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 border border-red-100 dark:border-red-800'
              }`}
            >
              {errorMsg}
              {status === 'error' && (
                <div className="text-xs mt-1 opacity-70">Tap above and try again</div>
              )}
            </div>
          )}

          <div className="mt-6 text-center">
            <a
              href="/setup"
              className="text-xs text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
            >
              First time? Run setup wizard →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
