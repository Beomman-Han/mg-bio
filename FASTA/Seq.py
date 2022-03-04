from typing import Type

class Seq:
    def __init__(self,
        type : str,
        data : str
        ) -> None:
        
        """Initializae Seq class with type, sequence.

        Parameters
        ----------
        type : str
            Type of sequence ('DNA' or 'RNA' or 'Protein')
        data : str
            Sequence string
        """
        
        self.type = type
        self.data = data
    
    def check(self) -> bool:
        """Check whether initialization is normal.

        Returns
        -------
        bool
            Is it normal content
        """
        ## IUPAC info was referred from http://www.incodom.kr/IUPAC
        BASE_IUPAC = {
            'A', 'C', 'G', 'T',
            'U', 'R', 'Y', 'M',
            'K', 'W', 'S', 'B',
            'D', 'H', 'V', 'N'
        }
        AMINO_ACID_IUPAC = {
            'A', 'R', 'N', 'D',
            'C', 'Q', 'E', 'G',
            'H', 'I', 'L', 'K',
            'M', 'F', 'P', 'S',
            'T', 'W', 'Y', 'V',
            'B', 'Z', 'X'
        }
        if self.type == 'DNA':
            DNA_IUPAC = BASE_IUPAC - {'U'}
            bases = list(set(self.data))
            for base in bases:
                if base not in DNA_IUPAC:
                    print('[WARNING] Sequence has weird character.')
                    print('[WARNING] Please check whether it is DNA sequence.')
                    print('[WARNING] It could raise errors at methods.')
                    return False
        elif self.type == 'RNA':
            RNA_IUPAC = BASE_IUPAC - {'T'}
            bases = list(set(self.data))
            for base in bases:
                if base not in RNA_IUPAC:
                    print('[WARNING] Sequence has weird character.')
                    print('[WARNING] Please check whether it is RNA sequence.')
                    print('[WARNING] It could raise errors at methods.')
                    return False
        elif self.type == 'Protein':
            amino_acids = list(set(self.data))
            for amino in amino_acids:
                if amino not in AMINO_ACID_IUPAC:
                    print('[WARNING] Sequence has weird character.')
                    print('[WARNING] Please check whether it is Protein sequence.')
                    print('[WARNING] It could raise errors at methods.')
                    return False
        else:
            print('[WARNING] It only supports DNA/RNA/Protein sequences.')
            return False
        return True
        
    def __repr__(self) -> str:
        """Represent Seq object by
        printing it's summary sequence data.

        Returns
        -------
        str
            Summary sequence data
        """
        
        if len(self.data) < 60:
            return f"Seq({self.data})"
        else:
            ## it would be better printing 60 char
            start = self.data[:30]
            end = self.data[-30:]
            return f"Seq({start}...{end})"       

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def complement(self) -> Type['Seq']:
        """Make complementary sequence of self.data.
        If Seq type is not DNA or RNA, it returns replicate object.

        Returns
        -------
        Seq
            Seq object which contains complementary sequence
        """
        
        IUPAC_PAIR = {"R": "Y", "Y": "R", "M": "K", "K": "M", "W": "W",
                    "S": "S", "B": "V", "V": "B", "D": "H", "H": "D"}
        if self.type == 'DNA':
            # watson_crick = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
            DNA_PAIR = {**{"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            for base in DNA_PAIR.keys():
                DNA_PAIR[base.lower()] = DNA_PAIR[base].lower()
            return Seq(self.type, "".join([DNA_PAIR[base] for base in self.data]))
        elif self.type == 'RNA':
            # watson_crick = {"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}
            RNA_PAIR = {**{"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            for base in RNA_PAIR.keys():
                RNA_PAIR[base.lower()] = RNA_PAIR[base].lower()
            return Seq(self.type, "".join([RNA_PAIR[base] for base in self.data]))
        else:
            print('[WARNING] Only DNA or RNA sequence can get complement seq.')
            ## return replicate Seq object
            return Seq(self.type, self.data)

    def reverse(self) -> Type['Seq']:
        """Make reverse sequence of self.data.

        Returns
        -------
        Seq
            Seq object which contains reverse sequence
        """

        return Seq(self.type, self.data[::-1])

    def get_data(self) -> str:
        return self.data

    def reverse_complement(self) -> Type['Seq']:
        """Make reverse complement sequence of self.data.
        If Seq type is not DNA or RNA, it returns reverse sequence.

        Returns
        -------
        Seq
            Seq object which contains reverse complement sequence
        """
        
        if self.type in ('DNA', 'RNA'):
            rev_com = self.complement().get_data()[::-1]
        else:
            rev_com = self.data[::-1]
        return Seq(self.type, rev_com)


if __name__ == "__main__":
    
    test_seq = 'ATGCTAGTCAGTCGTAGCTATTTGTACGTATCGATCTACTAGC'
    print(test_seq)
    
    temp = Seq(test_seq)
    print(temp.reverse_complemnt())