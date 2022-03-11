from typing import Dict, Type
from Constant import *

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
        
        if self.type == 'DNA':
            DNA_IUPAC = BASE_IUPAC - {'U'}
            bases = list(set(self.data.upper()))
            for base in bases:
                if base not in DNA_IUPAC:
                    print('[WARNING] Sequence has weird character.')
                    print('[WARNING] Please check whether it is DNA sequence.')
                    print('[WARNING] It could raise errors at methods.')
                    return False
        elif self.type == 'RNA':
            RNA_IUPAC = BASE_IUPAC - {'T'}
            bases = list(set(self.data.upper()))
            for base in bases:
                if base not in RNA_IUPAC:
                    print('[WARNING] Sequence has weird character.')
                    print('[WARNING] Please check whether it is RNA sequence.')
                    print('[WARNING] It could raise errors at methods.')
                    return False
        elif self.type == 'Protein':
            amino_acids = list(set(self.data.upper()))
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
        
        if len(self.data) <= 60:
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
        
        if self.type == 'DNA':
            # watson_crick = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
            DNA_PAIR = {**{"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            self._add_lower_case(DNA_PAIR)
            return Seq(self.type, "".join([DNA_PAIR[base] for base in self.data]))
        elif self.type == 'RNA':
            # watson_crick = {"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}
            RNA_PAIR = {**{"A": "U", "U": "A", "G": "C", "C": "G", "N": "N"}, **IUPAC_PAIR}
            self._add_lower_case(RNA_PAIR)
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

    def _has_iupac(self) -> bool:
        """Does self.data have IUPAC character 
        not 'ACGT(U)' base.

        Returns
        -------
        bool
            True if self.data has more than 'ACGT'
        """
        
        if self.type == 'DNA':
            if len(set(self.data) - {'A', 'C', 'G', 'T'}) != 0:
                return True
        elif self.type == 'RNA':
            if len(set(self.data) - {'A', 'C', 'G', 'U'}) != 0:
                return True
        return False
    
    def _warn_iupac(self) -> None:
        """Warn if self.data has more than 'ACGT(U)' base,
        it contains undecided IUPAC codes."""
        
        if self.type == 'DNA':
            if len(set(self.data) - {'A', 'C', 'G', 'T'}) != 0:
                # print('[WARNING] Sequence has more than A/C/G/T bases.')
                print('[WARNING] Sequence has undecided IUPAC codes.')
        elif self.type == 'RNA':
            if len(set(self.data) - {'A', 'C', 'G', 'U'}) != 0:
                # print('[WARNING] Sequence has more than A/C/G/U bases.')
                print('[WARNING] Sequence has undecided IUPAC codes.')
        return
    
    def count(self, char : str, verbose=True) -> int:
        """Count input char from self.data sequence.
        In case of DNA/RNA, it is recommended that 
        self.data have only 'ACGT(U)' not IUPAC character.
        Parameters
        ----------
        char : str
            Base or amino acid for counting
        verbose : bool, optional
            True, print warning message, by default True
        Returns
        -------
        int
            Count number
        """
        
        if verbose:
            self._warn_iupac()
        return self.data.upper().count(char.upper())
        
    def cal_gc_ratio(self, verbose=True) -> float or None:
        """Calculate GC ratio of self.data (only for DNA/RNA).
        GC ratio = ( count of G + count of C ) / length of seq
        Parameters
        ----------
        verbose : bool, optional
            True, print warning message, by default True
        Returns
        -------
        float or None
            GC ration or None for protein
        """
        
        if self.type == 'Protein':
            return None
        
        gc_count = self.count('G', verbose=False) + self.count('C', verbose=False)
        if verbose:
            self._warn_iupac()
        return gc_count / len(self.data)

    def _add_lower_case(self,
        dict : Dict[str, str]
        ) -> None:
        """Add lower case of keys at input dictionary.
        
        Example
        -------
        >>> dict
        {'A': 'T'}
        >>> self._add_lower_case(dict)
        >>> dict
        {'A': 'T', 'a': 't'}
        
        Parameters
        ----------
        dict : Dict[str, str]
            input dict like DNA_PAIR, RNA_PAIR, DNA_RNA_PAIR, etc.
        """
        
        for key in list(dict.keys()):
            dict[key.lower()] = dict[key].lower()

        return
        
    def transcribe(self, verbose=True) -> Type['Seq'] or None:
        """Transcribe DNA sequence to RNA sequence.
        
        Parameters
        ----------
        verbose : bool, optional
            Print warning message, by default True
        
        Returns
        -------
        Seq or None
            Seq object containing trancript or None
        """
        
        if self.type != 'DNA':
            if verbose:
                print('[WARNING] Transcription is only for DNA')
            return None
        if verbose:
            self._warn_iupac()
        DNA_RNA_PAIR = {**{'A': 'U', 'C': 'G', 'G': 'C', 'T': 'A'}, **IUPAC_PAIR}
        self._add_lower_case(DNA_RNA_PAIR)
        
        return Seq('RNA', ''.join([DNA_RNA_PAIR[base] for base in self.data])[::-1])
    
    def translate(self, verbose=True) -> Type['Seq'] or None:
        """Translate RNA sequence to protein sequence.
        
        Parameters
        ----------
        verbose : bool, optional
            Print warning message, by default True
        Returns
        -------
        Seq or None
            Seq object containing protein or None
        """
        
        if self.type != 'RNA':
            if verbose:
                print('[WARNING] Translation is only for RNA')
            return None
        if verbose:
            self._warn_iupac()
                
        ## find first 'AUG' sequence
        upper_data = self.data.upper()
        if len(set(upper_data) - {'A', 'C', 'G', 'U'}) != 0:
            return None
        
        start_idx = upper_data.index('AUG')
        protein = ""
        for i in range(start_idx, len(upper_data), 3):
            codon = upper_data[i:i+3]
            try:
                amino_acid = CODON_TABLE[codon]
                protein += amino_acid
                if amino_acid == "":
                    break
            except KeyError:
                break
        
        return Seq('Protein', protein)

    
if __name__ == "__main__":
    
    test_seq = 'ATGCTAGTCAGTCGTAGCTATTTGTACGTATCGATCTACTAGC'
    print(test_seq)
    
    temp = Seq('DNA', test_seq)
    # print(temp.check())
    # print(temp.complement())
    # print(temp.reverse())
    # print(temp.reverse_complement())
    # print(temp.count('a'))
    # print(temp.cal_gc_ratio())
    # print(temp.transcribe())
    print(temp._has_iupac())
    
    test_seq = 'AAAAAAAAAUGAUGAUGAUGUGAAAAAA'
    temp = Seq('RNA', test_seq)
    print(temp.translate())