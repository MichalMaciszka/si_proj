class Claster:
    def __init__(self, object_list):
        self.list = object_list
    
    def __str__(self):
        res = "Claster: \n"
        for x in self.list:
            res += str(x) + '\n'
        return res
    
    def compare(self, other_claster, hist, text):
        values = []
        for i in self.list:
            for j in other_claster.list:
                x, y = i.compare_offer(j)
                # val = x*y #? - ew x+y/2
                val = ((x*hist)+(y*text))/2
                # val = (x*hist)*(y*text)
                values.append(val)
        avg = 0
        for x in values:
            avg += x
        avg /= len(values)
        return avg
