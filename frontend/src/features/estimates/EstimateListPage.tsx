import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { estimatesApi, type EstimateResponse } from '../../api/estimates';
import { Button } from '../../components/common/Button';

export default function EstimateListPage() {
  const queryClient = useQueryClient();
  const [selectedEstimate, setSelectedEstimate] = useState<EstimateResponse | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ['estimates'],
    queryFn: estimatesApi.getAll
  });

  const approveMutation = useMutation({
    mutationFn: estimatesApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['estimates'] });
      setSelectedEstimate(null);
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Cost Estimates</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Internal cost estimations and markup pricing.
          </p>
        </div>
        <Link to="/estimates/new">
          <Button>+ Create Estimate</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Estimate No</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Total Cost</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Selling Value</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={6} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading Estimates...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={6} className="px-6 py-4 text-center text-sm text-muted-foreground">No Estimates found.</td></tr>
            ) : (
              data?.items.map((e) => (
                <tr key={e.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{new Date(e.estimate_date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{e.estimate_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${e.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 'bg-blue-100 text-blue-800'}`}>
                      {e.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-muted-foreground">₹{e.total_cost.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-bold text-foreground">₹{e.estimated_selling_value.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedEstimate(e)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {selectedEstimate && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-5xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedEstimate.estimate_number || 'Draft Estimate'}
                </h3>
                <p className="text-sm text-muted-foreground">Rev: {selectedEstimate.version}</p>
              </div>
              <button onClick={() => setSelectedEstimate(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border text-sm mb-6">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Item Name</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-red-50">Cost Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-red-50">Cost Amt</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-blue-50">Markup %</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-blue-50">Markup Amt</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-green-50">Sell Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-green-50">Sell Amt</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedEstimate.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">
                        {line.item_name_snapshot}
                        <div className="text-xs text-muted-foreground">{line.item_type}</div>
                      </td>
                      <td className="px-4 py-2 text-right">{line.quantity} {line.unit_snapshot}</td>
                      <td className="px-4 py-2 text-right text-red-700 bg-red-50">₹{line.cost_rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right font-medium text-red-700 bg-red-50">₹{line.cost_amount.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right text-blue-700 bg-blue-50">{line.markup_percent}%</td>
                      <td className="px-4 py-2 text-right text-blue-700 bg-blue-50">₹{line.markup_amount.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right text-green-700 bg-green-50">₹{line.selling_rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right font-medium text-green-700 bg-green-50">₹{line.selling_amount.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="grid grid-cols-2 gap-8 text-sm">
                <div className="border rounded p-4 bg-muted/50">
                  <h4 className="font-semibold mb-2">Cost Breakdown</h4>
                  <div className="flex justify-between"><span>Material</span><span>₹{selectedEstimate.material_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between"><span>Labour</span><span>₹{selectedEstimate.labour_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between"><span>Service</span><span>₹{selectedEstimate.service_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between"><span>Other</span><span>₹{selectedEstimate.other_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between font-bold pt-2 border-t mt-2"><span>Total Cost</span><span>₹{selectedEstimate.total_cost.toFixed(2)}</span></div>
                </div>
                
                <div className="border rounded p-4 bg-green-50">
                  <h4 className="font-semibold mb-2">Selling Breakdown</h4>
                  <div className="flex justify-between"><span>Total Cost</span><span>₹{selectedEstimate.total_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between text-blue-700"><span>Total Markup</span><span>+ ₹{selectedEstimate.markup_amount.toFixed(2)}</span></div>
                  <div className="flex justify-between font-bold pt-2 border-t mt-2 text-green-800 text-lg">
                    <span>Estimated Selling Value</span>
                    <span>₹{selectedEstimate.estimated_selling_value.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedEstimate(null)}>Close</Button>
              {selectedEstimate.status === 'DRAFT' && (
                <Button 
                  onClick={() => approveMutation.mutate(selectedEstimate.id)}
                  isLoading={approveMutation.isPending}
                >
                  Approve Estimate
                </Button>
              )}
              {selectedEstimate.status === 'APPROVED' && (
                <Link to={`/supply-out/quotations/new?estimate_id=${selectedEstimate.id}`}>
                  <Button variant="default">Create Quotation</Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
