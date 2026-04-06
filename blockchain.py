import hashlib
import os
import threading


class Transaction:
    def __init__(self, from_addr: str, to_addr: str, amount: float):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount


class Block:
    def __init__(self, index: int, previous_hash: str, transactions: list, difficulty: int):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.difficulty = difficulty
        self.nonce = -1
        self.hash = ""

    def build_block_data(self, nonce: int) -> str:
        tx_data = ""

        for tx in self.transactions:
            tx_data += f"{tx.from_addr}->{tx.to_addr}:{tx.amount:.8f};"

        return f"{self.index}|{self.previous_hash}|{tx_data}|{nonce}"

    @staticmethod
    def sha256(input_data: str) -> str:
        return hashlib.sha256(input_data.encode("utf-8")).hexdigest()

    def mine_parallel(self, miner_count: int):
        target = "0" * self.difficulty

        found = False
        lock = threading.Lock()

        result_nonce = -1
        result_hash = ""

        print(f"Mining block #{self.index} with {miner_count} miners...")
        print(f"Difficulty: {self.difficulty}")
        print()

        def miner_task(miner_id: int):
            nonlocal found, result_nonce, result_hash

            nonce = miner_id
            step = miner_count
            tries = 0

            while not found:
                data = self.build_block_data(nonce)
                current_hash = self.sha256(data)

                tries += 1

                if current_hash.startswith(target):
                    with lock:
                        if not found:
                            found = True
                            result_nonce = nonce
                            result_hash = current_hash

                            print(f"Miner #{miner_id} FOUND block #{self.index}!")
                            print(f"Nonce: {nonce}")
                            print(f"Hash : {current_hash}")
                            print(f"Tries: {tries}")
                            print()

                nonce += step

        threads = []

        for i in range(miner_count):
            t = threading.Thread(target=miner_task, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.nonce = result_nonce
        self.hash = result_hash

    def print_block(self):
        print("===== BLOCK =====")
        print(f"Index: {self.index}")
        print(f"Prev : {self.previous_hash}")
        print(f"Nonce: {self.nonce}")
        print(f"Hash : {self.hash}")
        print("Transactions:")

        for tx in self.transactions:
            print(f"- {tx.from_addr} -> {tx.to_addr} : {tx.amount:.8f} BTC")

        print("=================")
        print()


def main():
    difficulty = 2
    miner_count = os.cpu_count() or 4

    block_1_transactions = [
        Transaction("Bob", "Alice", 1.25),
        Transaction("Alice", "Charles", 0.40),
        Transaction("Charles", "Bob", 0.10),
        Transaction("Bob", "Charles", 0.75),
    ]

    block_1 = Block(
        1,
        "0000000000000000000000000000000000000000000000000000000000000000",
        block_1_transactions,
        difficulty
    )

    print("Before mining block 1:")
    block_1.print_block()
    block_1.mine_parallel(miner_count)
    print("After mining block 1:")
    block_1.print_block()

    block_2_transactions = [
        Transaction("Stefan", "Milica", 2.50),
        Transaction("Milica", "Nikola", 0.80),
        Transaction("Nikola", "Jovana", 1.10),
        Transaction("Jovana", "Stefan", 0.35),
    ]

    block_2 = Block(
        2,
        block_1.hash,
        block_2_transactions,
        difficulty
    )

    print("Before mining block 2:")
    block_2.print_block()
    block_2.mine_parallel(miner_count)
    print("After mining block 2:")
    block_2.print_block()

    block_3_transactions = [
        Transaction("Marko", "Ana", 3.20),
        Transaction("Ana", "Petar", 1.00),
        Transaction("Petar", "Ivana", 0.55),
        Transaction("Ivana", "Marko", 0.25),
    ]

    block_3 = Block(
        3,
        block_2.hash,
        block_3_transactions,
        difficulty
    )

    print("Before mining block 3:")
    block_3.print_block()
    block_3.mine_parallel(miner_count)
    print("After mining block 3:")
    block_3.print_block()

    block_4_transactions = [
        Transaction("Luka", "Teodora", 4.00),
        Transaction("Teodora", "Filip", 1.75),
        Transaction("Filip", "Sofija", 0.95),
        Transaction("Sofija", "Luka", 0.50),
    ]

    block_4 = Block(
        4,
        block_3.hash,
        block_4_transactions,
        difficulty
    )

    print("Before mining block 4:")
    block_4.print_block()
    block_4.mine_parallel(miner_count)
    print("After mining block 4:")
    block_4.print_block()

    print("Blockchain successfully created!")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()