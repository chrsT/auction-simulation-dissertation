import ENUMS, RANDOMS, PARAMETERS
class Genome(object):
    def __init__(self, genome_string):
        self.genes = {}
        genes_list = genome_string.split("-")

        #Version Check
        if genes_list[0] != PARAMETERS.VERSION:
            raise ValueError

        #Strategy
        self.genes["strategy"] = StrategyGene(StrategyGene.str_to_enum(genes_list[1]))

    @classmethod
    def CLASS_breed(self,genome_1,genome_2):
        new_genome = {}
        for gene in PARAMETERS.GENES:
            g1 = genome_1.get(gene)
            g2 = genome_2.get(gene)
            new_genome[gene] = g1.CLASS_breed(g1,g2)

        return PARAMETERS.GENOME_STRING.format(**new_genome)

    def get(self,gene):
        val = self.genes.get(gene,None)
        if val is None:
            return None
        return val

    def __str__(self):
        return PARAMETERS.GENOME_STRING.format(**self.genes)

class Gene(object):
    @classmethod
    def str_to_enum(self,str):
        raise NotImplementedError

    @classmethod
    def CLASS_breed(self, gene_1, gene_2):
        raise NotImplementedError

    @classmethod
    def mutate(self,val):
        raise NotImplementedError

    def __init__(self, value):
        self.value = value

    def __str__(self):
        raise NotImplementedError

    def get_value(self):
        return self.value


class StrategyGene(Gene):
    @classmethod
    def str_to_enum(self,str):
        if (str == "D"):
            return ENUMS.StrategyEnum.dove
        elif (str == "H"):
            return ENUMS.StrategyEnum.hawk
        raise ValueError

    @classmethod
    def enum_to_str(self,enum):
        if (enum == ENUMS.StrategyEnum.hawk):
            return "H"
        elif (enum == ENUMS.StrategyEnum.dove):
            return "D"
        else:
            raise ValueError

    @classmethod
    def CLASS_breed(self, gene_1, gene_2):
        val = 0
        if gene_1.get_value() == ENUMS.StrategyEnum.dove and gene_2.get_value() == ENUMS.StrategyEnum.dove:
            val = ENUMS.StrategyEnum.dove
        elif gene_1.get_value() == ENUMS.StrategyEnum.hawk and gene_2.get_value() == ENUMS.StrategyEnum.hawk:
            val = ENUMS.StrategyEnum.hawk
        else:
            val = RANDOMS.binary_random_decision(PARAMETERS.GENETICS_STRATEGY_HAWK_DOM,ENUMS.StrategyEnum.dove,ENUMS.StrategyEnum.hawk)

        val = self.mutate(val)

        return self.enum_to_str(val)

    @classmethod
    def mutate(self,val):
        mut = RANDOMS.binary_random_decision(PARAMETERS.GENETICS_STRATEGY_MUTATE,True, False)
        if mut:
            if val == ENUMS.StrategyEnum.hawk:
                return ENUMS.StrategyEnum.dove
            if val == ENUMS.StrategyEnum.dove:
                return ENUMS.StrategyEnum.hawk
            else:
                return
        return val

    def __init__(self, value):
        super(StrategyGene,self).__init__(value)
        self.type = ENUMS.GeneTypeEnum.distinct

    def __str__(self):
        if self.value == ENUMS.StrategyEnum.dove:
            return "D"
        elif self.value == ENUMS.StrategyEnum.hawk:
            return "H"
        raise ValueError