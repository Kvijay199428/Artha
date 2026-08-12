import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '../../api/auth';
import { useAuth } from '../../app/providers';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const loginSchema = z.object({
  pin: z.string().length(4, 'PIN must be exactly 4 digits').regex(/^\d+$/, 'PIN must contain only numbers'),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [apiError, setApiError] = useState<string | null>(null);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema)
  });

  const mutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: (response) => {
      login(response.data.token);
      navigate('/');
    },
    onError: (error: any) => {
      setApiError(error.message || 'Login failed. Please check your PIN.');
    }
  });

  const onSubmit = (data: LoginForm) => {
    setApiError(null);
    mutation.mutate(data);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-xl shadow-lg border border-gray-100">
        <div>
          <h2 className="mt-2 text-center text-3xl font-extrabold text-gray-900 tracking-tight">
            Artha Billing
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Enter your secure 4-digit PIN to access your company dashboard
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
          {apiError && (
            <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
              {apiError}
            </div>
          )}
          
          <div className="space-y-4">
            <Input
              label="Secure PIN"
              type="password"
              inputMode="numeric"
              maxLength={4}
              placeholder="••••"
              className="text-center text-2xl tracking-[0.5em] py-3"
              {...register('pin')}
              error={errors.pin?.message}
            />
          </div>

          <div>
            <Button
              type="submit"
              className="w-full py-3"
              isLoading={mutation.isPending}
            >
              Secure Login
            </Button>
          </div>
          
          <div className="text-center">
            <p className="text-sm text-gray-500">
              First time here? <a href="/setup" className="font-medium text-primary-600 hover:text-primary-500">Run setup wizard</a>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}
