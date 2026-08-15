import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Input } from '../ui/input';
import { Card } from '../ui/card';
import { invoicesApi, type InvoiceResponse } from '../../api/invoices';

interface Props {
  onSelect: (invoice: InvoiceResponse) => void;
  title?: string;
  transactionType?: 'SALES' | 'PURCHASE';
}

export function InvoiceReferenceSelector({ onSelect, title = "Select Source Invoice", transactionType = 'SALES' }: Props) {
  const [search, setSearch] = useState('');
  
  const { data, isLoading } = useQuery({
    queryKey: ['invoices', transactionType, search],
    queryFn: () => invoicesApi.getAll(transactionType),
  });

  const invoices = data?.items?.filter((inv: any) => 
    inv.invoice_number.toLowerCase().includes(search.toLowerCase()) ||
    inv.customer_name_snapshot.toLowerCase().includes(search.toLowerCase())
  ) || [];

  return (
    <div className="max-w-2xl mx-auto space-y-6 mt-8">
      <div>
        <h2 className="text-2xl font-bold">{title}</h2>
        <p className="text-muted-foreground">Search by Invoice Number or Customer/Supplier</p>
      </div>

      <Input 
        placeholder="Search..." 
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full text-lg p-6"
      />

      <div className="space-y-4">
        {isLoading ? (
          <p>Loading...</p>
        ) : (
          invoices.map((inv: any) => (
            <Card key={inv.id} className="p-4 hover:border-primary cursor-pointer transition-colors" onClick={() => onSelect(inv)}>
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-bold text-lg">{inv.invoice_number}</h3>
                  <p className="text-muted-foreground">{inv.customer_name_snapshot}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium">₹{inv.grand_total.toFixed(2)}</p>
                  <p className="text-sm text-muted-foreground">{inv.invoice_date}</p>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
