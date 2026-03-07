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
  const [status, setStatus] = useState<string>('Loading settings...')

  useEffect(() => {
    const load = async () => {
      try {
        const settings = await getAISettings()
        setStyle(settings.response_style)
        setSelectedModel(settings.model ?? '')
        setStatus(
          settings.has_openai_api_key
            ? `Stored API key: ${settings.openai_api_key_masked ?? 'hidden'}`
            : 'No API key configured'
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
      setStatus('AI settings saved.')
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
      setStatus(`Loaded ${loaded.length} models.`)
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    }
  }

  return (
    <div className="page-container">
      <FeaturePanel title="AI configuration" lead="OpenAI key, model discovery, response style">
        <form className="form" onSubmit={handleSave}>
          <label className="form__field">
            <span>OpenAI API key</span>
            <input
              type="password"
              value={apiKey}
              onChange={(event) => setApiKey(event.target.value)}
              placeholder="sk-..."
            />
          </label>
          <label className="form__field">
            <span>Response style</span>
            <select
              value={style}
              onChange={(event) => setStyle(event.target.value as 'concise' | 'balanced' | 'detailed')}
            >
              <option value="concise">Concise</option>
              <option value="balanced">Balanced</option>
              <option value="detailed">Detailed</option>
            </select>
          </label>
          <label className="form__field">
            <span>OpenAI model</span>
            <select value={selectedModel} onChange={(event) => setSelectedModel(event.target.value)}>
              <option value="">Select model</option>
              {models.map((model) => (
                <option key={model} value={model}>
                  {model}
                </option>
              ))}
            </select>
          </label>
          <div className="form__actions">
            <button type="button" className="secondary-button" onClick={handleTestKey}>
              Test API key
            </button>
            <button type="button" className="secondary-button" onClick={handleLoadModels}>
              Load models
            </button>
            <button type="submit" className="primary-button">
              Save settings
            </button>
          </div>
        </form>
        <StatusMessage variant="empty" title="AI settings status" description={status} />
      </FeaturePanel>
    </div>
  )
}
