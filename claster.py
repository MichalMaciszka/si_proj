class Claster:
    def __init__(self, object_list):
        self.list = object_list
    
    def __str__(self):
        res = "Claster: \n"
        for x in self.list:
            res += x.__str__() + '\n'
        return res
    
    def compare(self, other_claster):
        values = []
        for i in self.list:
            for j in other_claster.list:
                x, y = i.compare_offer(j)
                val = x*y #? - ew x+y*2
                values.append(val)
        avg = 0
        for x in values:
            avg += x
        avg /= len(values)
        return avg