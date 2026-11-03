import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Progress } from '@/components/ui/progress';
import { Switch } from '@/components/ui/switch';
import { Checkbox } from '@/components/ui/checkbox';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';
import { Table, TableHeader, TableBody, TableHead, TableRow, TableCell } from '@/components/ui/table';
import {
  Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from '@/components/ui/dialog';
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select';
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel,
  DropdownMenuSeparator, DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';

/**
 * Styleguide — /?styleguide
 *
 * Every primitive on one page, in the current theme. This is the page you
 * screenshot when judging "is the theme applied everywhere?", and the page to
 * extend whenever a new primitive is added. Not linked from the app.
 */
const swatches = [
  ['background', 'bg-background', 'border-border'],
  ['foreground', 'bg-foreground', ''],
  ['card', 'bg-card', 'border-border'],
  ['primary', 'bg-primary', ''],
  ['secondary', 'bg-secondary', ''],
  ['muted', 'bg-muted', ''],
  ['accent', 'bg-accent', ''],
  ['destructive', 'bg-destructive', ''],
  ['border', 'bg-border', ''],
];

const Section = ({ title, children }) => (
  <section className="flex flex-col gap-4">
    <h2 className="text-lg font-semibold text-foreground">{title}</h2>
    <div className="flex flex-wrap items-start gap-3">{children}</div>
    <Separator />
  </section>
);

export default function StyleGuide() {
  const [dark, setDark] = useState(() => document.documentElement.classList.contains('dark'));
  const [progress, setProgress] = useState(40);

  const toggle = () => {
    const next = !dark;
    setDark(next);
    document.documentElement.setAttribute('data-theme', next ? 'dark' : 'light');
    document.documentElement.classList.toggle('dark', next);
  };

  return (
    <div className="min-h-screen bg-background p-8 text-foreground">
      <div className="mx-auto flex max-w-5xl flex-col gap-8">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold">ARTHA UI kit</h1>
            <p className="text-sm text-muted-foreground">
              shadcn/ui primitives on the ARTHA token layer — every colour below comes from
              <code className="mx-1 rounded bg-muted px-1 py-0.5 text-xs">src/styles/tokens.css</code>.
            </p>
          </div>
          <Button variant="outline" onClick={toggle}>
            {dark ? 'Switch to Light' : 'Switch to Dark'}
          </Button>
        </header>

        <Section title="Tokens">
          <div className="grid grid-cols-3 gap-3 sm:grid-cols-5">
            {swatches.map(([label, cls, border]) => (
              <div key={label} className="flex flex-col gap-1">
                <div className={`h-14 w-full rounded-md border ${cls} ${border || 'border-transparent'}`} />
                <span className="text-xs text-muted-foreground">{label}</span>
              </div>
            ))}
          </div>
        </Section>

        <Section title="Buttons">
          <Button>Default</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="outline">Outline</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="destructive">Destructive</Button>
          <Button variant="link">Link</Button>
          <Button size="sm">Small</Button>
          <Button size="lg">Large</Button>
          <Button disabled>Disabled</Button>
        </Section>

        <Section title="Badges">
          <Badge>Default</Badge>
          <Badge variant="secondary">Secondary</Badge>
          <Badge variant="outline">Outline</Badge>
          <Badge variant="destructive">Destructive</Badge>
        </Section>

        <Section title="Form controls">
          <div className="grid w-full max-w-md gap-4">
            <div className="grid gap-2">
              <Label htmlFor="sg-name">Business name</Label>
              <Input id="sg-name" placeholder="Acme Traders" />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="sg-notes">Notes</Label>
              <Textarea id="sg-notes" placeholder="Payment terms…" />
            </div>
            <div className="grid gap-2">
              <Label>GST rate</Label>
              <Select defaultValue="18">
                <SelectTrigger>
                  <SelectValue placeholder="Pick a rate" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">0%</SelectItem>
                  <SelectItem value="5">5%</SelectItem>
                  <SelectItem value="12">12%</SelectItem>
                  <SelectItem value="18">18%</SelectItem>
                  <SelectItem value="28">28%</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-center gap-2">
              <Checkbox id="sg-check" defaultChecked />
              <Label htmlFor="sg-check">Tax inclusive prices</Label>
            </div>
            <div className="flex items-center gap-2">
              <Switch id="sg-switch" defaultChecked />
              <Label htmlFor="sg-switch">Round off total</Label>
            </div>
            <RadioGroup defaultValue="b2b" className="flex gap-6">
              {['b2b', 'b2c'].map((v) => (
                <div key={v} className="flex items-center gap-2">
                  <RadioGroupItem value={v} id={`sg-radio-${v}`} />
                  <Label htmlFor={`sg-radio-${v}`}>{v.toUpperCase()}</Label>
                </div>
              ))}
            </RadioGroup>
          </div>
        </Section>

        <Section title="Card">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>This month</CardTitle>
              <CardDescription>Revenue after returns</CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <div className="text-2xl font-bold">₹1,28,054.20</div>
              <Progress value={progress} />
              <Input
                type="range"
                min="0"
                max="100"
                value={progress}
                onChange={(e) => setProgress(Number(e.target.value))}
                className="h-2 border-0 bg-transparent p-0 shadow-none"
              />
            </CardContent>
            <CardFooter className="justify-end gap-2">
              <Button variant="outline" size="sm">Export</Button>
              <Button size="sm">Open</Button>
            </CardFooter>
          </Card>
        </Section>

        <Section title="Overlays">
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline">Open dialog</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Delete this invoice?</DialogTitle>
                <DialogDescription>
                  INV/2026-27/0042 will be removed from this company. This cannot be undone.
                </DialogDescription>
              </DialogHeader>
              <DialogFooter>
                <Button variant="outline">Cancel</Button>
                <Button variant="destructive">Delete</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>

          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline">Dropdown</Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start">
              <DropdownMenuLabel>Invoice</DropdownMenuLabel>
              <DropdownMenuItem>Edit</DropdownMenuItem>
              <DropdownMenuItem>Duplicate</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem variant="destructive">Delete</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <Button variant="ghost">Tooltip</Button>
              </TooltipTrigger>
              <TooltipContent>Saved locally</TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </Section>

        <Section title="Tabs &amp; table">
          <div className="w-full">
            <Tabs defaultValue="all">
              <TabsList>
                <TabsTrigger value="all">All</TabsTrigger>
                <TabsTrigger value="unpaid">Unpaid</TabsTrigger>
                <TabsTrigger value="paid">Paid</TabsTrigger>
              </TabsList>
              <TabsContent value="all">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Client</TableHead>
                      <TableHead>Invoice</TableHead>
                      <TableHead className="text-right">Total</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    <TableRow>
                      <TableCell>Sharma Interiors</TableCell>
                      <TableCell>INV/2026-27/0041</TableCell>
                      <TableCell className="text-right">₹18,880.00</TableCell>
                    </TableRow>
                    <TableRow data-state="selected">
                      <TableCell>Patel Hardware</TableCell>
                      <TableCell>INV/2026-27/0042</TableCell>
                      <TableCell className="text-right">₹4,130.00</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TabsContent>
              <TabsContent value="unpaid">Nothing unpaid.</TabsContent>
              <TabsContent value="paid">Nothing paid.</TabsContent>
            </Tabs>
          </div>
        </Section>
      </div>
    </div>
  );
}
