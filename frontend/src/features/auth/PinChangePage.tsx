import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '../../api/auth';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const pinChangeSchema = z.object({
  old_pin: z.string().length(4, 'PIN must be exactly 4 digits'),
  new_pin: z.string().length(4, 'PIN must be exactly 4 digits').regex(/^\d+$/, 'PIN must contain only numbers'),
  confirm_pin: z.string().length(4, 'PIN must be exactly 4 digits'),
}).refine((data) => data.new_pin === data.confirm_pin, {
  message: "New PINs don't match",
  path: ["confirm_pin"],
});

type PinChangeForm = z.infer<typeof pinChangeSchema>;

export default function PinChangePage() {
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const { register, handleSubmit, formState: { errors }, reset } = useForm<PinChangeForm>({
    resolver: zodResolver(pinChangeSchema)
  });

  const mutation = useMutation({
    mutationFn: authApi.changePin,
    onSuccess: () => {
      setSuccess(true);
      reset();
      navigate('/');
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to change PIN.');
    }
  });

  const onSubmit = (data: PinChangeForm) => {
    setApiError(null);
    setSuccess(false);
    mutation.mutate(data);
  };

  return (
    <div className="max-w-md mx-auto space-y-8 bg-card p-10 rounded-xl shadow border mt-12">
      <div>
        <h2 className="text-2xl font-bold text-foreground tracking-tight">
          Change Security PIN
        </h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Update your 4-digit PIN for dashboard access.
        </p>
      </div>
      
      <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
        {apiError && (
          <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
            {apiError}
          </div>
        )}
        {success && (
          <div className="bg-green-50 text-green-600 p-3 rounded-md text-sm border border-green-100">
            PIN changed successfully! Redirecting...
          </div>
        )}
        
        <div className="space-y-4">
          <Input
            label="Current PIN"
            type="password"
            maxLength={4}
            {...register('old_pin')}
            error={errors.old_pin?.message}
          />
          <Input
            label="New PIN"
            type="password"
            maxLength={4}
            {...register('new_pin')}
            error={errors.new_pin?.message}
          />
          <Input
            label="Confirm New PIN"
            type="password"
            maxLength={4}
            {...register('confirm_pin')}
            error={errors.confirm_pin?.message}
          />
        </div>

        <div className="flex space-x-3 pt-2">
          <Button
            type="button"
            variant="secondary"
            className="w-full"
            onClick={() => navigate('/')}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            className="w-full"
            isLoading={mutation.isPending}
          >
            Update PIN
          </Button>
        </div>
      </form>
    </div>
  );
}
