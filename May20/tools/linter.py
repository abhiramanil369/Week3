import asyncio
import tempfile
import subprocess

class PylintLinterTool:
    name="linter"

    async def lint(self,code:str) ->str:
        loop=asyncio.get_event_loop()
        return await loop.run_in_executor(None,self._lint_sync,code)
    
    def _lint_sync(self,code:str)->str:
        with tempfile.NamedTemporaryFile(suffix='.py',mode='w',delete=False) as f:
            f.write(code)
            temp_path=f.name

        try:
            result=subprocess.run(
                ["pylint",temp_path,"--disable=all","--enable=E,W,F"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return result.stdout + result.stderr
        finally:
            import os
            os.remove(temp_path)
            