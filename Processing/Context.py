class Context:
    def __init__(self):
        self.files = {}
        self.parameters = {}

    def add_file(self, key, file_path):
        self.files[key] = file_path

    def get_file(self, key):
        return self.files.get(key)

    def has_file(self, key):
        return key in self.files

    def add_parameters(self, key, params):
        self.parameters[key] = params

    def get_parameters(self, key):
        return self.parameters.get(key, [])

    def has_parameter(self, key):
        return key in self.parameters