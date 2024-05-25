from src.domain.learn.lstm import LearnLSTMModel


class InstanceLSTMFirstModule(LearnLSTMModel):
    version = "0.0.1"
    name = "lstm_first"
    input_size: int
    hidden_size: int
    num_layers: int
    output_size: int

    def __init__(self, input_size=8, hidden_size=512, num_layers=2, output_size=1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.output_size = output_size

        super().__init__(self.input_size, self.hidden_size, self.num_layers, self.output_size)
