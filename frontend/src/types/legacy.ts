export type LegacyTransactionType = 'income' | 'expense'

export type LegacyCategory =
  | 'Salary'
  | 'Food'
  | 'Utilities'
  | 'Transport'
  | 'Entertainment'

export interface LegacyTransaction {
  id: number
  date: string
  description: string
  category: LegacyCategory
  amount: number
  type: LegacyTransactionType
}
