class ClassSignature:
    def __init__(
            self,
            member_count: int,
            method_count: int,
            instructions_count: int,
            members_simhash: int,
            methods_params_simhash: int,
            method_returns_simhash: int,
            instructions_simhash: int,
    ):
        self.member_count = member_count
        self.method_count = method_count
        self.instructions_count = instructions_count
        self.members_simhash = members_simhash
        self.methods_params_simhash = methods_params_simhash
        self.methods_returns_simhash = method_returns_simhash
        self.instructions_simhash = instructions_simhash