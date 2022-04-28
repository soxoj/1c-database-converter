import asyncio
import logging
import onec_dtools
import os
from json import JSONEncoder
from typing import List, Any

from aiohttp import TCPConnector, ClientSession

from .executor import AsyncioProgressbarQueueExecutor, AsyncioSimpleExecutor


class InputData:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class OutputData:
    def __init__(self, ftype, value, status, error):
        self.out_file = value
        self.file_type = ftype
        self.status = status
        self.error = error

    @property
    def fields(self):
        fields = list(self.__dict__.keys())
        fields.remove('error')

        return fields

    def __str__(self):
        error = ''
        if self.error:
            error = f' (error: {str(self.error)}'

        result = ''

        for field in self.fields:
            field_pretty_name = field.title().replace('_', ' ')
            value = self.__dict__.get(field)
            if value:
                result += f'{field_pretty_name}: {str(value)}\n'

        result += f'{error}'
        return result


class OutputDataList:
    def __init__(self, input_data: InputData, results: List[OutputData]):
        self.input_data = input_data
        self.results = results

    def __repr__(self):
        return f'Target {self.input_data}:\n' + '--------\n'.join(map(str, self.results))


class OutputDataListEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, OutputDataList):
            return {'input': o.input_data, 'output': o.results}
        elif isinstance(o, OutputData):
            return {k:o.__dict__[k] for k in o.fields}
        else:
            return o.__dict__


class Processor:
    def __init__(self, *args, **kwargs):
        from aiohttp_socks import ProxyConnector

        # make http client session
        proxy = kwargs.get('proxy')
        self.proxy = proxy
        if proxy:
            connector = ProxyConnector.from_url(proxy, ssl=False)
        else:
            connector = TCPConnector(ssl=False)

        self.session = ClientSession(
            connector=connector, trust_env=True
        )
        if kwargs.get('no_progressbar'):
            self.executor = AsyncioSimpleExecutor()
        else:
            self.executor = AsyncioProgressbarQueueExecutor()

        self.logger = logging.getLogger('processor')

    async def close(self):
        await self.session.close()


    def onec_tables_csv_export(self, filename, output_dir):
        with open(filename, 'rb') as f:
            db = onec_dtools.DatabaseReader(f)
            tables = db.tables.items()
            for i in tables:
                output_filename = os.path.join(output_dir, i[0]+'.csv')
                output_file = open(output_filename, 'w')

                for row in i[1]:
                    if row.is_empty:
                        continue
                    fields = row.as_list(True)
                    new_fields = []
                    for field in fields:
                        if type(field) == bytes:
                            new_fields.append('<BINARY DATA>')
                        else:
                            new_fields.append(str(field))

                    output_file.write(';'.join(new_fields))

                output_file.close()

    async def request(self, input_data: InputData) -> OutputDataList:
        from bs4 import BeautifulSoup as bs
        status = 0
        file_type = 'unknown'
        result = None
        error = None

        try:
            filename = input_data.value

            if filename.lower().endswith('.cf'):
                file_type = 'CF'
                result = filename + '_unpack'
                if os.path.exists(result):
                    status = f'Not exported, directory {result} exists!'
                else:
                    onec_dtools.extract(filename, result)
                    status = 'Exported content of CF file'
            elif filename.lower().endswith('.1cd'):
                file_type = '1CD'
                result = filename + '_csv'
                if os.path.exists(result):
                    status = f'Not exported, directory {result} exists!'
                else:
                    os.mkdir(result)
                    self.onec_tables_csv_export(filename, result)
                    status = 'Exported content of 1CD file'

        except Exception as e:
            self.logger.error(e, exc_info=True)

        await asyncio.sleep(0)

        results = OutputDataList(input_data, [OutputData(file_type, result, status, error)])

        return results


    async def process(self, input_data: List[InputData]) -> List[OutputDataList]:
        tasks = [
            (
                self.request, # func
                [i],          # args
                {}            # kwargs
            )
            for i in input_data
        ]

        results = await self.executor.run(tasks)

        return results
