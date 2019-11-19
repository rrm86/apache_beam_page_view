'''
Autor : Ronnald Rezende Machado
Job para encontrar
carrinhos abandonados
pelos clientes de um e-commerce
'''
import json
import logging
import time
import datetime
import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.io import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions


class Abandono(beam.DoFn):

    def process(self, element):
        '''
        Localiza
        o abandono.
        Os dados estão
        agrupados por sessão
        de 10 minutos
        e por usuário.

        Parametros:
        element(tuple)
        '''
        usuario = element[0]
        saida = list()

        # obtem páginas visitadas
        paginas = [page['page'] for page in element[1]]

        # verifica se o usuario foi até o checkout
        if 'checkout' not in paginas:
            saida.append(element[1])

        tamanho = len(saida)
        if tamanho > 0:
            logging.warning('O Usuario %s teve um abandono detectado', usuario)
            # obtem o último item da lista
            saida = saida[0][tamanho-1]
            yield saida


def salva_arquivo(item):
    '''
    Cria o arquivo de 
    saida ou adiciona
    novas informacoes
    caso o mesmo
    ja exista
    '''
    agora = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(agora)
    with open('output/abandoned-carts.json', 'a') as fp:
        json.dump(item, fp)


def parse_json(item):
    '''
    Executa o parse
    do json
    Parametros:
    item(str)
    '''
    yield json.loads(item)


def run(argv=None):
    '''
    Processa
    os dados
    '''

    p = beam.Pipeline(options=PipelineOptions())

    # 10 minutos
    sessao = 60*10

    with beam.Pipeline(options=PipelineOptions()) as p:

        carrinho = (p
            | 'Lê Arquivo' >> ReadFromText('input/page-views.json')
            | 'Transforma entrada' >> beam.ParDo(parse_json)
            | 'Adiciona Timestamp' >> beam.Map(
                lambda x: beam.window.TimestampedValue(
                x,datetime.datetime.strptime(
                    x['timestamp'],  
                    '%Y-%m-%d %H:%M:%S').timestamp()))
            | 'Adciona chave' >> beam.Map(lambda x: (x['customer'], x))
            | 'Define Sessão'>> beam.WindowInto(
                window.Sessions(sessao),
                timestamp_combiner=window.TimestampCombiner.OUTPUT_AT_EOW)
            | 'Group By Key' >> beam.GroupByKey()
            | 'Verifica Abandono' >> beam.ParDo(Abandono())
            | 'Salva Saida' >> beam.ParDo(salva_arquivo)
            )


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    logging.info('Executando processamento...')
    run()
    logging.info('Fim do processamento...')
