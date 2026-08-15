import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { boqsApi, type BOQResponse } from '../../api/boqs';
import { Button } from '../../components/common/Button';

export default function BOQListPage() {
  const queryClient = useQueryClient();
  const [selectedBOQ, setSelectedBOQ] = useState<BOQResponse | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ['boqs'],
    queryFn: boqsApi.getAll
  });

  const approveMutation = useMutation({
    mutationFn: boqsApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['boqs'] });
      setSelectedBOQ(null);
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Bills of Quantities (BOQ)</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your project BOQs and structural estimates.
          </p>
        </div>
        <Link to="/boqs/new">
          <Button>+ Create BOQ</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">BOQ No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Project Name</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={5} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading BOQs...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={5} className="px-6 py-4 text-center text-sm text-muted-foreground">No BOQs found.</td></tr>
            ) : (
              data?.items.map((b) => (
                <tr key={b.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{new Date(b.boq_date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{b.boq_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{b.project_name || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${b.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 'bg-blue-100 text-blue-800'}`}>
                      {b.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedBOQ(b)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {selectedBOQ && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedBOQ.boq_number || 'Draft BOQ'}
                </h3>
                <p className="text-sm text-muted-foreground">Project: {selectedBOQ.project_name} | Rev: {selectedBOQ.version}</p>
              </div>
              <button onClick={() => setSelectedBOQ(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border text-sm mb-6">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Type</th>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Description</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Est. Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Est. Amount</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedBOQ.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2 text-xs font-semibold text-muted-foreground">{line.item_type}</td>
                      <td className="px-4 py-2">
                        {line.description}
                        {line.quantity_formula && <div className="text-xs text-blue-500">Formula: {line.quantity_formula}</div>}
                      </td>
                      <td className="px-4 py-2 text-right">{line.quantity} {line.unit_snapshot}</td>
                      <td className="px-4 py-2 text-right text-muted-foreground">₹{line.estimated_rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right font-medium">₹{line.estimated_amount.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot className="bg-muted/50">
                  <tr>
                    <td colSpan={4} className="px-4 py-2 text-right font-bold">Total Estimated Value</td>
                    <td className="px-4 py-2 text-right font-bold text-lg">
                      ₹{selectedBOQ.lines.reduce((sum, l) => sum + l.estimated_amount, 0).toFixed(2)}
                    </td>
                  </tr>
                </tfoot>
              </table>
              {selectedBOQ.notes && (
                <div className="mt-4 p-4 bg-muted text-foreground text-sm rounded">
                  <strong>Notes:</strong> {selectedBOQ.notes}
                </div>
              )}
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedBOQ(null)}>Close</Button>
              {selectedBOQ.status === 'DRAFT' && (
                <Button 
                  onClick={() => approveMutation.mutate(selectedBOQ.id)}
                  isLoading={approveMutation.isPending}
                >
                  Approve BOQ
                </Button>
              )}
              {selectedBOQ.status === 'APPROVED' && (
                <Link to={`/estimates/new?boq_id=${selectedBOQ.id}`}>
                  <Button variant="default">Create Estimate</Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
