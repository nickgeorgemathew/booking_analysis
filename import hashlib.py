import hashlib
import time
import json
import random
import string

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        class Transaction:
            def __init__(self, sender, recipient, amount, sender_private_key=None, timestamp=None):
                self.sender = sender  # address (public key) or "SYSTEM" for mining rewards
                self.recipient = recipient
                self.amount = amount
                self.timestamp = timestamp or time.time()
                # In this toy system we include the sender's private key for authorization.
                # This is insecure in real systems but keeps this example self-contained.
                self.sender_private_key = sender_private_key

            def to_dict(self):
                return {
                    "sender": self.sender,
                    "recipient": self.recipient,
                    "amount": self.amount,
                    "timestamp": self.timestamp,
                    "sender_private_key": self.sender_private_key,
                }

            def __repr__(self):
                return json.dumps(self.to_dict(), sort_keys=True)


        class Block:
            def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
                self.index = index
                self.previous_hash = previous_hash
                self.timestamp = timestamp
                self.transactions = transactions  # list of Transaction
                self.nonce = nonce
                self.hash = self.calculate_hash()

            def calculate_hash(self):
                tx_str = "".join([repr(tx) for tx in self.transactions])
                block_string = f"{self.index}{self.previous_hash}{self.timestamp}{tx_str}{self.nonce}"
                return hashlib.sha256(block_string.encode()).hexdigest()

            def mine_block(self, difficulty):
                target = '0' * difficulty
                while self.hash[:difficulty] != target:
                    self.nonce += 1
                    self.hash = self.calculate_hash()


        class Wallet:
            @staticmethod
            def create_wallet():
                # private key: random hex string; public key (address): sha256(private)
                private = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
                public = hashlib.sha256(private.encode()).hexdigest()
                return {"private_key": private, "address": public}


        class Blockchain:
            def __init__(self, difficulty=2, mining_reward=50):
                self.chain = [self.create_genesis_block()]
                self.difficulty = difficulty
                self.pending_transactions = []
                self.mining_reward = mining_reward

            def create_genesis_block(self):
                genesis_tx = Transaction("SYSTEM", "genesis", 0)
                return Block(0, "0", time.time(), [genesis_tx])

            def get_latest_block(self):
                return self.chain[-1]

            def add_transaction(self, transaction):
                # Basic validation:
                if transaction.sender != "SYSTEM":
                    if not transaction.sender_private_key:
                        raise ValueError("Missing sender private key for authorization.")
                    # verify private -> public
                    expected_address = hashlib.sha256(transaction.sender_private_key.encode()).hexdigest()
                    if expected_address != transaction.sender:
                        raise ValueError("Invalid private key for sender address.")
                    # check balance
                    if self.get_balance(transaction.sender) < transaction.amount:
                        raise ValueError("Insufficient balance.")
                if transaction.amount <= 0:
                    raise ValueError("Transaction amount must be positive.")
                self.pending_transactions.append(transaction)

            def mine_pending_transactions(self, miner_address):
                # reward transaction from SYSTEM
                reward_tx = Transaction("SYSTEM", miner_address, self.mining_reward)
                block_transactions = self.pending_transactions + [reward_tx]
                new_block = Block(
                    index=self.get_latest_block().index + 1,
                    previous_hash=self.get_latest_block().hash,
                    timestamp=time.time(),
                    transactions=block_transactions
                )
                new_block.mine_block(self.difficulty)
                self.chain.append(new_block)
                self.pending_transactions = []

            def get_balance(self, address):
                balance = 0
                for block in self.chain:
                    for tx in block.transactions:
                        if tx.sender == address:
                            balance -= tx.amount
                        if tx.recipient == address:
                            balance += tx.amount
                # pending transactions should be considered when showing available balance
                for tx in self.pending_transactions:
                    if tx.sender == address:
                        balance -= tx.amount
                    if tx.recipient == address:
                        balance += tx.amount
                return balance

            def is_chain_valid(self):
                # validate hashes and transaction authorizations and that no double-spend occurs
                balances = {}
                for i, block in enumerate(self.chain):
                    # hash check
                    if block.hash != block.calculate_hash():
                        return False
                    if i > 0 and block.previous_hash != self.chain[i - 1].hash:
                        return False
                    # process transactions and verify
                    for tx in block.transactions:
                        sender = tx.sender
                        recipient = tx.recipient
                        amount = tx.amount

                        if sender != "SYSTEM":
                            if not tx.sender_private_key:
                                return False
                            expected_address = hashlib.sha256(tx.sender_private_key.encode()).hexdigest()
                            if expected_address != sender:
                                return False
                        # apply balances
                        balances.setdefault(sender, 0)
                        balances.setdefault(recipient, 0)
                        if sender != "SYSTEM":
                            if balances[sender] < amount:
                                return False
                            balances[sender] -= amount
                        balances[recipient] += amount
                return True


        # Example usage:
        if __name__ == "__main__":
            # create wallets
            alice = Wallet.create_wallet()
            bob = Wallet.create_wallet()
            miner = Wallet.create_wallet()

            print("Alice:", alice)
            print("Bob:", bob)
            print("Miner:", miner)
            print()

            blockchain = Blockchain(difficulty=3, mining_reward=100)

            # Miner mines the first block to collect reward
            blockchain.mine_pending_transactions(miner["address"])
            print("Miner balance after first mining:", blockchain.get_balance(miner["address"]))

            # Alice receives some coins from SYSTEM (simulated faucet)
            faucet_tx = Transaction("SYSTEM", alice["address"], 150)
            blockchain.add_transaction(faucet_tx)
            blockchain.mine_pending_transactions(miner["address"])
            print("Alice balance after faucet:", blockchain.get_balance(alice["address"]))
            print("Miner balance:", blockchain.get_balance(miner["address"]))

            # Alice sends Bob 40 coins (includes private key for authorization)
            tx1 = Transaction(sender=alice["address"], recipient=bob["address"], amount=40, sender_private_key=alice["private_key"])
            blockchain.add_transaction(tx1)
            # Mine to include the transaction
            blockchain.mine_pending_transactions(miner["address"])

            print("Alice balance:", blockchain.get_balance(alice["address"]))
            print("Bob balance:", blockchain.get_balance(bob["address"]))
            print("Miner balance:", blockchain.get_balance(miner["address"]))

            print("\nBlockchain valid?", blockchain.is_chain_valid())

            # print chain summary
            for block in blockchain.chain:
                print("-" * 40)
                print(f"Index: {block.index}")
                print(f"Hash: {block.hash}")
                print(f"Previous Hash: {block.previous_hash}")
                print("Transactions:")
                for tx in block.transactions:
                    print(" ", tx.to_dict())
                print(f"Nonce: {block.nonce}")
                print(f"Timestamp: {block.timestamp}")
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            index=previous_block.index + 1,
            previous_hash=previous_block.hash,
            timestamp=time.time(),
            data=data
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# Example usage:
if __name__ == "__main__":
    blockchain = Blockchain(difficulty=3)
    blockchain.add_block("First block data")
    blockchain.add_block("Second block data")

    for block in blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Hash: {block.hash}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Data: {block.data}")
        print(f"Nonce: {block.nonce}")
        print(f"Timestamp: {block.timestamp}")
        print("-" * 40)