=(Get-Location).Path
='sqlite+aiosqlite:///./backend/tests/test.db'
='redis://localhost:6379/1'
='test-secret'
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=''
python -m pytest backend
