import React, { useEffect, useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'
import { listAccounts, searchMessages, unwrapApiError } from '@services/api'
import type { AccountRead, SearchResult } from '@services/api'

export const SearchPage = () => {
  const [accounts, setAccounts] = useState<AccountRead[]>([])
  const [selectedAccount, setSelectedAccount] = useState<number | null>(null)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [status, setStatus] = useState('Načítám účty…')
  const [searching, setSearching] = useState(false)

  useEffect(() => {
    const load = async () => {
      try {
        const loaded = await listAccounts()
        setAccounts(loaded)
        setSelectedAccount(loaded[0]?.id ?? null)
        setStatus(loaded.length ? 'Vyberte dotaz a spusťte hledání.' : 'Přidejte nejprve účet.')
      } catch (error) {
        setStatus(unwrapApiError(error).message)
      }
    }
    load()
  }, [])

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!selectedAccount) {
      setStatus('Vyberte účet pro dotaz.')
      return
    }
    if (!query.trim()) {
      setStatus('Zadejte hledanou frázi.')
      return
    }
    setSearching(true)
    setStatus('Hledám zprávy…')
    try {
      const found = await searchMessages({ account_id: selectedAccount, q: query.trim() })
      setResults(found)
      setStatus(found.length ? `Nalezeno ${found.length} zpráv.` : 'Žádné výsledky.')
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    } finally {
      setSearching(false)
    }
  }

  return (
    <div className="page-container">
      <FeaturePanel title="Hledání" lead="Vyhledávejte v propojených účtech">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>Účet</span>
            <select
              value={selectedAccount ?? ''}
              onChange={(event) => setSelectedAccount(event.target.value ? Number(event.target.value) : null)}
            >
              <option value="" disabled>
                Vyberte účet
              </option>
              {accounts.map((account) => (
                <option key={account.id} value={account.id}>
                  {account.email}
                </option>
              ))}
            </select>
          </label>
          <label className="form__field">
            <span>Vyhledávací dotaz</span>
            <input
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder='"Důležité" AND projekt'
            />
          </label>
          <button className="primary-button" type="submit" disabled={searching}>
            {searching ? 'Hledám…' : 'Spustit hledání'}
          </button>
        </form>
        <StatusMessage variant="empty" title="Výsledek hledání" description={status} />
        {results.length > 0 && (
          <ul className="search-results">
            {results.map((result) => (
              <li key={result.id} className="search-results__item">
                <p className="search-results__subject">{result.subject}</p>
                <p className="search-results__snippet">{result.body ?? 'Žádný text'}</p>
                <p className="search-results__meta">{result.created_at}</p>
              </li>
            ))}
          </ul>
        )}
      </FeaturePanel>
    </div>
  )
}
