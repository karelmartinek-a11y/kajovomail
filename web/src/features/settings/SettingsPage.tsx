import React, { useEffect, useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'
import {
  getAISettings,
  listOpenAIModels,
  testOpenAIKey,
  unwrapApiError,
  updateAISettings,
} from '@services/api'

export const SettingsPage = () => {
  const [apiKey, setApiKey] = useState('')
  const [style, setStyle] = useState<'concise' | 'balanced' | 'detailed'>('balanced')
  const [selectedModel, setSelectedModel] = useState('')
  const [models, setModels] = useState<string[]>([])
  const [status, setStatus] = useState<string>('Načítám nastavení...')

  useEffect(() => {
    const load = async () => {
      try {
        const settings = await getAISettings()
        setStyle(settings.response_style)
        setSelectedModel(settings.model ?? '')
        setStatus(
          settings.has_openai_api_key
            ? `Uložený API klíč: ${settings.openai_api_key_masked ?? 'skrytý'}`
            : 'API klíč zatím není nastaven'
        )
      } catch (error) {
        setStatus(unwrapApiError(error).message)
      }
    }
    load()
  }, [])

  const handleSave = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    try {
      await updateAISettings({
        openai_api_key: apiKey.trim() || undefined,
        response_style: style,
        model: selectedModel || undefined,
      })
      setApiKey('')
      setStatus('AI nastavení bylo uloženo.')
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    }
  }

  const handleTestKey = async () => {
    try {
      const result = await testOpenAIKey(apiKey.trim() || undefined)
      setStatus(result.message)
      if (result.models.length > 0) {
        setModels(result.models)
        if (!selectedModel) {
          setSelectedModel(result.models[0])
        }
      }
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    }
  }

  const handleLoadModels = async () => {
    try {
      const loaded = await listOpenAIModels()
      setModels(loaded)
      if (loaded.length > 0 && !selectedModel) {
        setSelectedModel(loaded[0])
      }
      setStatus(`Načteno modelů: ${loaded.length}.`)
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    }
  }

  return (
    <div className="page-container">
      <FeaturePanel title="AI konfigurace" lead="OpenAI klíč, načtení modelů, styl odpovědi">
        <form className="form" onSubmit={handleSave}>
          <label className="form__field">
            <span>OpenAI API klíč</span>
            <input
              type="password"
              value={apiKey}
              onChange={(event) => setApiKey(event.target.value)}
              placeholder="sk-..."
            />
          </label>
          <label className="form__field">
            <span>Styl odpovědi</span>
            <select
              value={style}
              onChange={(event) => setStyle(event.target.value as 'concise' | 'balanced' | 'detailed')}
            >
              <option value="concise">Stručný</option>
              <option value="balanced">Vyvážený</option>
              <option value="detailed">Detailní</option>
            </select>
          </label>
          <label className="form__field">
            <span>OpenAI model</span>
            <select value={selectedModel} onChange={(event) => setSelectedModel(event.target.value)}>
              <option value="">Vyberte model</option>
              {models.map((model) => (
                <option key={model} value={model}>
                  {model}
                </option>
              ))}
            </select>
          </label>
          <div className="form__actions">
            <button type="button" className="secondary-button" onClick={handleTestKey}>
              Otestovat API klíč
            </button>
            <button type="button" className="secondary-button" onClick={handleLoadModels}>
              Načíst modely
            </button>
            <button type="submit" className="primary-button">
              Uložit nastavení
            </button>
          </div>
        </form>
        <StatusMessage variant="empty" title="Stav AI nastavení" description={status} />
      </FeaturePanel>
    </div>
  )
}
