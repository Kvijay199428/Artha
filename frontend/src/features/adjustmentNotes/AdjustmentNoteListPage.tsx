import { useQuery } from '@tanstack/react-query';
import { adjustmentNotesApi, type AdjustmentNoteResponse } from '../../api/adjustmentNotes';
import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/button';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  createColumnHelper
} from '@tanstack/react-table';

const columnHelper = createColumnHelper<AdjustmentNoteResponse>();

export default function AdjustmentNoteListPage({ noteType }: { noteType: 'CREDIT_NOTE' | 'DEBIT_NOTE' }) {
  const { data, isLoading } = useQuery({
    queryKey: ['adjustmentNotes', noteType],
    queryFn: () => adjustmentNotesApi.getAll(noteType),
  });

  const columns = [
    columnHelper.accessor('note_number', {
      header: 'Note Number',
      cell: info => info.getValue(),
    }),
    columnHelper.accessor('note_date', {
      header: 'Date',
      cell: info => new Date(info.getValue()).toLocaleDateString(),
    }),
    columnHelper.accessor('grand_total', {
      header: 'Amount',
      cell: info => `₹${info.getValue().toFixed(2)}`,
    }),
    columnHelper.accessor('status', {
      header: 'Status',
      cell: info => <span className="uppercase text-xs font-semibold">{info.getValue()}</span>,
    }),
    columnHelper.display({
      id: 'actions',
      cell: info => (
        <Link to={`/${noteType === 'CREDIT_NOTE' ? 'credit-notes' : 'debit-notes'}/${info.row.original.id}`}>
          <Button variant="outline" size="sm">View</Button>
        </Link>
      )
    })
  ];

  const table = useReactTable({
    data: data?.items || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">
          {noteType === 'CREDIT_NOTE' ? 'Credit Notes' : 'Debit Notes'}
        </h1>
        <Link to={`/${noteType === 'CREDIT_NOTE' ? 'credit-notes' : 'debit-notes'}/new`}>
          <Button>Create {noteType === 'CREDIT_NOTE' ? 'Credit Note' : 'Debit Note'}</Button>
        </Link>
      </div>

      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <div className="border rounded-md">
          <table className="w-full text-sm text-left">
            <thead className="bg-muted">
              {table.getHeaderGroups().map(headerGroup => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map(header => (
                    <th key={header.id} className="p-3 font-semibold border-b">
                      {flexRender(header.column.columnDef.header, header.getContext())}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody>
              {table.getRowModel().rows.map(row => (
                <tr key={row.id} className="border-b hover:bg-muted/50">
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} className="p-3">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
