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

        #Rep weighting
        self.genes["rep_weighting"] = RepWeightingGene(genes_list[2])

        #Prob defect
        self.genes["prob_defect"] = ProbDefectGene(genes_list[3])

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
        dict = {}
        for k, v in self.genes.items():
            dict[k] = v.genome_string()
        return PARAMETERS.GENOME_STRING.format(**dict)

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

    def genome_string(self):
        raise NotImplementedError


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

    def genome_string(self):
        return str(self)

class RepWeightingGene(Gene):
    def __init__(self,value):
        super(RepWeightingGene,self).__init__(value)
        self.type = ENUMS.GeneTypeEnum.int
        self.value = int(value)

    @classmethod
    def CLASS_breed(self, gene_1, gene_2):
        g1 = gene_1.get_value()
        g2 = gene_2.get_value()

        val = int((g1 + g2) / 2)

        val = self.mutate(val)

        if (val < 0):
            val = 0

        if (val > 1023):
            val = 1023

        return int(val)

    @classmethod
    def mutate(self,val):
        val += RANDOMS.random_int(PARAMETERS.GENETICS_REP_WEIGHTING_MUTATE_ADD[0],PARAMETERS.GENETICS_REP_WEIGHTING_MUTATE_ADD[1])

        if val == 0:
            val = 1023

        for m in PARAMETERS.GENETICS_REP_WEIGHTING_MUTATE_FLIP:
            if RANDOMS.binary_random_decision((1024/m),True,False):
                div, mod = divmod(m, val)
                if (div % 2 == 0):
                    val += m
                else:
                    val -= m

        return val

    def __str__(self):
        pass

    @classmethod
    def str_to_enum(self,str):
        pass

    def genome_string(self):
        return str(self.get_value())

class ProbDefectGene(Gene):
    def __init(self,value):
        super(ProbDefectGene,self).__init__(value)
        self.type = ENUMS.GeneTypeEnum.int
        self.value = int(value)

    @classmethod
    def CLASS_breed(self, gene_1, gene_2):
        g1 = int(gene_1.get_value())
        g2 = int(gene_2.get_value())

        val = int((g1 + g2) / 2)

        val = self.mutate(val)

        if (val < 0):
            val = 0

        if (val > 1023):
            val = 1023

        return int(val)

    @classmethod
    def mutate(self,val):
        val += RANDOMS.random_int(PARAMETERS.GENETICS_PROB_DEFECT_MUTATE_ADD[0],PARAMETERS.GENETICS_PROB_DEFECT_MUTATE_ADD[1])

        if val == 0:
            val = 1023

        for m in PARAMETERS.GENETICS_PROB_DEFECT_MUTATE_FLIP:
            if RANDOMS.binary_random_decision((1024/m),True,False):
                div, mod = divmod(m, val)
                if (div % 2 == 0):
                    val += m
                else:
                    val -= m

        return val

    def __str__(self):
        pass

    @classmethod
    def str_to_enum(self,str):
        pass

    def genome_string(self):
        return str(self.get_value())