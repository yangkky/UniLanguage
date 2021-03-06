import argparse
import gzip
import urllib.parse
import urllib.request
import subprocess
import multiprocessing

import numpy as np

parser = argparse.ArgumentParser(description='Download the protein datasets')
parser.add_argument('--data', type=str, default='data/', help='location of the data ids')
parser.add_argument('--domain', choices=['euk', 'bac', 'arc', 'vir'], default='euk',
                    help='domain of origin: "euk","bac","arc" or "vir"')
parser.add_argument('--complete', choices=['full', 'frag'], default='full',
                    help='completeness of the protein: "full" or "frag"')
parser.add_argument('--quality', choices=['exp', 'pred'], default='exp',
                    help='evidence of existence of the protein: "exp" or "pred"')
parser.add_argument('--all', help='downloads all the data', action='store_true')

args = parser.parse_args()

all_domains = ['euk', 'bac', 'arc', 'vir']
all_complete = ['full', 'frag']
all_quality = ['exp', 'pred']


def download_set(loc, domain, complete, quality, dataset):
    header = 'Downloading %s %s %s %s set...' % (domain, complete, quality, dataset)
    url = 'https://www.uniprot.org/uploadlists/'
    query = [line.rstrip('\n') for line in
             gzip.open('%s/%s_%s_%s/%s_ids.txt.gz' % (loc, domain, complete, quality, dataset), 'rt')]

    n_total = len(query)

    n = 3000
    fname = '%s/%s_%s_%s/%s.txt' % (loc, domain, complete, quality, dataset)
    formated_file = open(fname, 'a')
    # See how long file is already and jump ahead if necessary
    current_length = int(subprocess.check_output('wc -l < ' + fname, shell=True)[:-1])
    i = int(np.ceil(current_length / n))
    while i * n < n_total:
        tmp_query = query[i * n:i * n + n]
        tmp_query = ' '.join(tmp_query)
        params = {
            'from': 'ACC+ID',
            'to': 'ACC',
            'format': 'tab',
            'columns': 'sequence',
            'query': tmp_query
        }

        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data)

        attempt = 1
        j = i * n + 1
        k = (i + 1) * n
        try:
            print(header + 'Attempt no %d for sequences %d through %d of %d' % (attempt, j, k, n_total))
            with urllib.request.urlopen(req) as f:
                f.readline()
                seqs = []
                for line in f:
                    line = line.decode('utf-8').strip().split('\t')
                    seq = ''.join(list(line[0]))
                    formated_file.write('%s\n' % seq)
                    seqs.append(seq)
            i += 1
        except urllib.error.HTTPError:
            attempt += 1

    formated_file.close()
    print()


if args.all:
    print('Downloading all the data...')
    n_proc = multiprocessing.cpu_count()
    f_args = []
    for domain in all_domains:
        for complete in all_complete:
            for quality in all_quality:
                f_args.append((args.data, domain, complete, quality, 'train'))
                f_args.append((args.data, domain, complete, 'exp', 'valid'))
                f_args.append((args.data, domain, complete, 'exp', 'test'))
    with multiprocessing.Pool(n_proc) as pool:
        result = pool.starmap_async(download_set, f_args)
        result.get()


else:
    print('Downloading %s %s %s train, valid and test sets...' % (args.domain, args.complete, args.quality))
    download_set(args.data, args.domain, args.complete, args.quality, 'train')
    download_set(args.data, args.domain, args.complete, 'exp', 'valid')
    download_set(args.data, args.domain, args.complete, 'exp', 'test')

print('Download complete')
