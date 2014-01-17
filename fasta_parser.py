class Seq(object):

    def __init__(self,key,records_dict):
        self.key = key
        self.records = records_dict

    def tostring(self):
        s = self.records[self.key]['sequence']
        return s.replace('\n','')


class SeqRecord(object):

    def __init__(self,key,records_dict):
        self.records = records_dict
        self.key = key
        self.seq = Seq(key,records_dict)

    def format(self,out_format):
        if out_format == 'fasta':
            r = self.records[self.key]
            return ">%s\n%s" % (r['description'],r['sequence'])


class FastaParser(object):

    def __init__(self,fasta_file):
        self.fasta_file = fasta_file
        fasta = open(fasta_file,'r').read()
        self.entries = [x for x in fasta.split('>') if len(x) != 0]
        self.build_records_dict()

    def keys(self):
        keys_list = []
        for entry in self.entries:
            key = [x for x in entry.split('\n')[0].split() if len(x) != 0][0]
            keys_list.append(key)
        return [x.strip() for x in keys_list]

    def __len__(self):
        return len(self.keys())

    def __iter__(self):
        for k in self.keys():
            yield k

    def build_records_dict(self):
        records_dict = {}
        for entry in self.entries:
            key = [x for x in entry.split('\n')[0].split() if len(x) != 0][0]
            description = entry.split('\n')[0]
            sequence = '\n'.join(entry.split('\n')[1:]).strip()
            records_dict[key] = {'description':description,'sequence':sequence}
        self.records = records_dict

    def __getitem__(self,key):
        return SeqRecord(key,self.records)