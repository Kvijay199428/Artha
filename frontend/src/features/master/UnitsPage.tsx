import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { unitsApi } from '../../api/units';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const unitSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  abbreviation: z.string().min(1, 'Abbreviation is required'),
  category: z.string().min(1, 'Category is required'),
  is_base_unit: z.boolean(),
  base_unit_id: z.string().optional(),
  multiplier: z.coerce.number().optional(),
  formula: z.string().optional(),
  aliases: z.string().optional(),
});

type UnitForm = z.infer<typeof unitSchema>;

export default function UnitsPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const { data: units = [], isLoading } = useQuery({
    queryKey: ['units'],
    queryFn: unitsApi.getAll
  });

  const { register, handleSubmit, watch, formState: { errors }, reset } = useForm<any>({
    resolver: zodResolver(unitSchema),
    defaultValues: {
      is_base_unit: true,
      multiplier: 1
    }
  });

  const isBaseUnit = watch('is_base_unit');

  const createMutation = useMutation({
    mutationFn: unitsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
      setIsModalOpen(false);
      reset();
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create unit');
    }
  });

  const deleteMutation = useMutation({
    mutationFn: unitsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
    }
  });

  const onSubmit = (data: any) => {
    setApiError(null);
    createMutation.mutate({
      ...(data as UnitForm),
      base_unit_id: data.base_unit_id ? parseInt(data.base_unit_id) : null,
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Units of Measurement</h2>
          <p className="mt-1 text-sm text-muted-foreground">Manage base units, derived units, and custom conversion formulas.</p>
        </div>
        <Button onClick={() => setIsModalOpen(true)}>Add New Unit</Button>
      </div>

      {isLoading ? (
        <div>Loading units...</div>
      ) : (
        <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
          <table className="min-w-full divide-y divide-border">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Unit</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Abbreviation</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Formula / Multiplier</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {units.map((unit) => (
                <tr key={unit.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">{unit.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{unit.abbreviation}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{unit.category}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    {unit.is_base_unit ? (
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Base</span>
                    ) : (
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">Derived</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    {unit.formula ? (
                      <code className="text-xs bg-muted px-1 py-0.5 rounded">{unit.formula}</code>
                    ) : unit.multiplier !== 1 ? (
                      `${unit.multiplier}x Base`
                    ) : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button 
                      onClick={() => {
                        if (confirm('Are you sure you want to delete this unit?')) {
                          deleteMutation.mutate(unit.id);
                        }
                      }}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity bg-black/60" onClick={() => setIsModalOpen(false)}></div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
            <div className="inline-block px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-card rounded-xl shadow-xl sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
              <h3 className="text-lg font-medium leading-6 text-foreground mb-4">Add New Unit</h3>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                {apiError && (
                  <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
                    {apiError}
                  </div>
                )}
                
                <div className="grid grid-cols-2 gap-4">
                  <Input label="Name (e.g. Kilogram)" {...register('name')} error={errors.name?.message} />
                  <Input label="Abbreviation (e.g. KG)" {...register('abbreviation')} error={errors.abbreviation?.message} />
                </div>
                
                <Input label="Category (e.g. Weight)" {...register('category')} error={errors.category?.message} />
                
                <div className="flex items-center h-10 mt-2">
                  <input type="checkbox" id="is_base_unit" className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-input rounded" {...register('is_base_unit')} />
                  <label htmlFor="is_base_unit" className="ml-2 block text-sm text-foreground font-medium">This is a Base Unit</label>
                </div>

                {!isBaseUnit && (
                  <div className="space-y-4 p-4 bg-muted rounded-md border border">
                    <div>
                      <label className="block text-sm font-medium text-muted-foreground mb-1">Base Unit Reference</label>
                      <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('base_unit_id')}>
                        <option value="">Select a base unit...</option>
                        {units.filter(u => u.is_base_unit).map(u => (
                          <option key={u.id} value={u.id}>{u.name} ({u.abbreviation})</option>
                        ))}
                      </select>
                    </div>
                    <Input label="Simple Multiplier (e.g. 1000)" type="number" step="any" {...register('multiplier')} error={errors.multiplier?.message} />
                    <Input label="Or Custom Formula (e.g. PCS * 1.5)" {...register('formula')} error={errors.formula?.message} />
                  </div>
                )}

                <Input label="Aliases (comma separated)" placeholder="kg, kgs, kilo" {...register('aliases')} error={errors.aliases?.message} />

                <div className="mt-5 sm:mt-6 flex justify-end space-x-3">
                  <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                  <Button type="submit" isLoading={createMutation.isPending}>Save Unit</Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
