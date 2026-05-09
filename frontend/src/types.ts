export type TransactionType = 'income' | 'expense';

export type Category =
  | 'Salary'
  | 'Food'
  | 'Utilities'
  | 'Transport'
  | 'Entertainment';

export interface Transaction {
  id: number;
  date: string;
  description: string;
  category: Category;
  amount: number;
  type: TransactionType;
}
