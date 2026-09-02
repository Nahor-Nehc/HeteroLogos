from Phoneme import Phoneme

#! move to components once completed


class PhonemeDistanceRow:
    def __init__(self, row_data:list[float|int], row_headers:list[str]):
        self._dict = {}
        
        if len(row_data) != len(row_headers):
            raise ValueError(f"row_data {len(row_data)} and row_headers \
                {len(row_headers)} have mismatched lengths")
        
        for i in range(len(row_data)):
            self._dict[row_headers[i]] = float(row_data[i])

    def __getitem__(self, item) -> float:
        if isinstance(item, Phoneme):
            item = item.string
                    
        if item not in self._dict.keys():
            raise ValueError(f"item '{item}' not in PhonemeDistanceRow:\n{str(self)}")

        return self._dict[item]
    
    def __str__(self):
        return str(self._dict)


class PhonemeDistanceMatrix:
    def __init__(self, filepath:str):
        """
        Supposes the file is a matrix with the phonemes in the first row and column
    
        :param filepath: path to the csv file
        :type filepath: str
        """
        self._dict = {}
        
        with open(filepath) as f:
            data = f.readlines()
        
        headers = data[0].strip().split(",")[1:]
        for line in data[1:]:
            phoneme, *values = line.strip().split(",")
            row = PhonemeDistanceRow(values, headers)
            self._dict[phoneme] = row
        
        
    def __getitem__(self, item) -> PhonemeDistanceRow:
        # accept either a raw phoneme string or an object with a `string` attribute
        if isinstance(item, Phoneme):
            item = item.string
        
        if item not in self._dict.keys():
            raise ValueError(f"item '{item}' not in PhonemeDistanceMatrix:\n{str(self)}")

        return self._dict[item]
    
    def __str__(self) -> str:
        s = ""
        for phoneme, values in self._dict.items():
            s += f"{phoneme}: {str(values)}\n"
        return s