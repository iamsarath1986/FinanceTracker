export type AccountType = 'savings' | 'investments' | 'checking' | 'credit_card' | 'cash'
export type CategoryType = 'income' | 'expense'
export type TransactionType = 'income' | 'expense'
export type Frequency = 'daily' | 'weekly' | 'monthly' | 'yearly'
export type ScopeType = 'category' | 'account'
export type PeriodType = 'monthly' | 'annual'

export interface Account {
  id: number
  name: string
  type: AccountType
  bank_name: string | null
  country: string | null
  currency: string
  opening_balance: number
  current_balance: number
  created_at: string
  updated_at: string
}

export interface Category {
  id: number
  name: string
  type: CategoryType
  color: string | null
  icon: string | null
  created_at: string
  updated_at: string
}

export interface Transaction {
  id: number
  account_id: number
  category_id: number | null
  amount: number
  type: TransactionType
  date: string
  description: string | null
  is_recurring: boolean
  recurring_id: number | null
  created_at: string
}

export interface RecurringTransaction {
  id: number
  account_id: number
  category_id: number | null
  amount: number
  type: TransactionType
  description: string | null
  frequency: Frequency
  start_date: string
  end_date: string | null
  last_generated_date: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Budget {
  id: number
  name: string
  scope_type: ScopeType
  period_type: PeriodType
  category_id: number | null
  account_id: number | null
  year: number
  month: number | null
  limit_amount: number
  currency: string
  spent: number
}

export interface DashboardSummary {
  accounts: { id: number; name: string; currency: string; current_balance: number }[]
  monthly_cashflow: { month: string; income: number; expense: number }[]
  budget_progress: { budget_id: number; name: string; limit_amount: number; spent: number; currency: string }[]
  recent_transactions: Transaction[]
}
