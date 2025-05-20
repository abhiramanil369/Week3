import asyncio
import sys
import traceback

class PythonExecutorTool:
    name="executor"

    async def execute(self,code: str)->str:
        loop=asyncio.get_event_loop()
        return await loop.run_in_executor(None,self._run_code,code)
    
    def _run_code(self,code:str)->str:
        try:
            import io
            old_stdout=sys.stdout
            sys.stdout=mystdout=io.StringIO()
            exec(code,{})
            sys.stdout=old_stdout
            return mystdout.getvalue()
        except Exception:
            return traceback.format_exc()