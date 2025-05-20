import tempfile
import subprocess
import os
import asyncio

class PylintLinterTool:
    name = "linter"

    async def lint(self, code: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._lint_sync, code)

    def _lint_sync(self, code: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as f:
            f.write(code)
            temp_path = f.name
        try:
            result = subprocess.run(
                ["pylint", temp_path, "--disable=all", "--enable=E,W,F"],
                capture_output=True, text=True
            )
            return result.stdout + "\n" + result.stderr
        finally:
            os.unlink(temp_path)