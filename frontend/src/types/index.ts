export interface User {
  user_id: string
  email: string
  name: string
  is_active: boolean
  created_at: string
}

export interface Category {
  category_id: string
  user_id: string
  name: string
  emoji?: string
  color: string
  created_at: string
  updated_at: string
}

export interface Expense {
  expense_id: string
  user_id: string
  category_id: string
  title: string
  amount: number
  date: string
  note?: string
  is_recurring: boolean
  created_at: string
  updated_at: string
}

export interface Budget {
  budget_id: string
  user_id: string
  category_id: string
  monthly_limit: number
  alert_threshold: number
  created_at: string
  updated_at: string
  spent?: number
  percentage?: number
  is_alert?: boolean
  is_exceeded?: boolean
}

export interface RecurringExpense {
  recurring_id: string
  user_id: string
  expense_id: string
  frequency: 'weekly' | 'monthly' | 'yearly'
  is_active: boolean
  last_execution_date?: string
  created_at: string
  updated_at: string
}

export interface ApiToken {
  token_id: string
  name: string
  scopes: string[]
  is_active: boolean
  last_used?: string
  created_at: string
}

export interface DashboardData {
  stats: {
    total: string
    today: string
    month: number
    year: number
    currency: string
  }
  breakdown: Array<{
    category_id: string
    category_name: string
    emoji?: string
    color: string
    amount: number
    percentage: number
  }>
  trend: Array<{
    month: number
    year: number
    amount: number
  }>
  budget_summary?: {
    total_budgets: number
    budgets_alert: number
    budgets_exceeded: number
  }
}
