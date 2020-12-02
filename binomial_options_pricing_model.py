from math import exp, sqrt

class BinomialOptionsPricingModel:
    class OptionType:
        CALL="CALL"
        PUT="PUT"
    
    class OptionStyle:
        AMERICAN_STYLE="AMERICAN"
        EUROPEAN="EUROPEAN"

    class Node:
        def __init__(self, S0, u, Nu, Nd):
            self.S = S0 * pow(u, Nu-Nd)
            self.XV = None
            self.BV = None
            self.OV = None

    def __init__(self, inputs):

        self.option_type = inputs["option_type"].upper()
        self.option_style = inputs["option_style"].upper()

        self.S0 = inputs["stock_price"]
        self.X = inputs["strike_price"]
        self.r = inputs["risk_free_interest_rate"]
        self.u = inputs["up_factor"]
        self.d = inputs["down_factor"]
        self.T = inputs["T"]
        self.t = inputs["time_periods"]

        self.p = self.calc_prob(self.r, self.t, self.u, self.d)
        self.lattice = self.generate_lattice(self.S0, self.u, self.t)
        curr_value = self.backward_induction(self.lattice, self.calc_exercise_val(self.lattice, self.X, self.option_type))

    def get_inputs(self):
        return inputs
    
    def get_present_value(self):
        return self.lattice[0][0].OV

    def calc_up_factor(self, sigma, t, n):
        return pow(exp(sigma * sqrt(t/n)))

    def calc_down_factor(self, u):
        return (1/u)

    def calc_binomial_value(self, Vu, Vd, p, r, t):
        F = (p * Vu) + ((1-p) * Vd)
        i = pow(1+r, t)
        return F/i

    def calc_prob(self, r, t, u, d):
        mu = pow((1 + r), t)
        sigma = u - d 
        return (mu - d)/sigma

    def set_option_val(self, node):
        node.OV = max(node.BV, node.XV if node.XV is not None else 0)

    def generate_lattice(self, S0, u, t):
        # r = # of u
        # c = # of d
        lattice = [
            [ self.Node(S0, u, c, r) for c in range(t + 1 - r) ]
            for r in range(t + 1)
        ]
        return lattice

    def calc_exercise_val(self, lattice, X, option_type):
        nodes = []
        for c, row in enumerate(lattice):
            X_node = row[-1]
            nodes.append((c, len(row) - 1))
            if option_type == self.OptionType.CALL:
                X_node.XV = round(max((X_node.S - X), 0), 2)

            elif option_type == self.OptionType.PUT:
                X_node.XV = round(max(0, (X - X_node.S)), 2)

            X_node.OV = X_node.XV
        return nodes
        

    def backward_induction(self, lattice, nodes):
        back_nodes = set()

        for loc in nodes:
            r = loc[0]
            c = loc[1] - 1

            if c < 0:
                continue
            back_nodes.add((r,c))

        for coord in back_nodes:
            r, c = coord
            t = min(r, c)
            p = self.calc_prob(self.r, t, self.u, self.d)

            curr_node = lattice[r][c]
            up_node = lattice[r][c+1]
            down_node = lattice[r+1][c]

            up_value = up_node.XV if up_node.BV is None else up_node.BV
            down_value = down_node.XV if down_node.BV is None else down_node.BV

            BV = self.calc_binomial_value(up_value, down_value, p, self.r, t)
            curr_node.BV = round(BV, 2)
            self.set_option_val(curr_node)

        if back_nodes:
            return self.backward_induction(self.lattice, back_nodes)
        else:
            return self.lattice[0][0].BV

    def print_lattice(self, results_type):
        print("Lattice Results Value type: {}".format(results_type))
        for r in range(self.t + 1):
            for c in range(self.t + 1 - r):
                if results_type == "S":
                    results = self.lattice[r][c].S
                elif results_type == "XV":
                    results = self.lattice[r][c].XV
                elif results_type == "BV":
                    results= self.lattice[r][c].BV
                elif results_type == "OV":
                    results = self.lattice[r][c].OV
                print("\t{}".format(results), end="")
            print()
        print()

if __name__ == "__main__":
    from json import dumps
    inputs = {
        "option_style": "american",
        "option_type": "call",
        "stock_price": 100,
        "strike_price": 120,
        "volatility": 0.316,
        "risk_free_interest_rate": 0.0009,
        "up_factor": 1.25,
        "down_factor": 0.80,
        "T": 1,
        "time_periods": 2
    }

    BOPM = BinomialOptionsPricingModel(inputs)
    print(dumps(BOPM.get_inputs(), indent=2))

    BOPM.print_lattice("S")
    BOPM.print_lattice("BV")
    BOPM.print_lattice("XV")
    BOPM.print_lattice("OV")
    print("Present Option Value = {}".format(BOPM.get_present_value()))

