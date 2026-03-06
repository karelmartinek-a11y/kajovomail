import palette from '@brand/palette/palette.json'
import tokens from '@brand/ui-tokens/tokens.json'

type Primitive = string | number | boolean | null

type FlatEntry = {
  key: string
  value: Primitive
}

const flattenObject = (value: unknown, path: string[] = []): FlatEntry[] => {
  if (value === null || typeof value !== 'object') {
    return [{ key: path.join('-'), value: value as Primitive }]
  }

  return Object.entries(value as Record<string, unknown>).flatMap(([key, nested]) =>
    flattenObject(nested, [...path, key])
  )
}

const applyFlatEntries = (root: HTMLElement, prefix: string, entries: FlatEntry[]) => {
  entries.forEach(({ key, value }) => {
    root.style.setProperty(`--${prefix}-${key}`, String(value))
  })
}

export const applyBrandTokens = () => {
  const root = document.documentElement
  applyFlatEntries(root, 'brand-palette', flattenObject(palette))
  applyFlatEntries(root, 'brand-tokens', flattenObject(tokens))
}
