# GZFLS Blockchain Project



`product` store the previous version of project.

`buildVersion` is the current version of project we are working on

`test` will have some fancy implementation that we may add into project in the future.



## Program Sequence Diagram

### Process to Create A New Transaction

```mermaid
sequenceDiagram
	TerminalAgent ->> TaskQueue: Create Transaction A
	TaskQueue ->> TaskDistributor: Get Task
	TaskDistributor ->> Worker: Distribute "CREATE_TX" Task to Worker
	Worker ->> Worker: Create New Transaction
	Worker ->> TaskQueue: New Task Registered:<br>{to:"miner", instruction:"ADD_TX", args:"TxA.serialize()"}
	Worker ->> TaskQueue: New Task Registered:<br>{to:"webAgent", instruction:"SEND_TX", args:"TxA.serialize()"}
	TaskQueue ->> TaskDistributor: Get Task
	TaskDistributor ->> Miner: Distribute "ADD_TX" Task to Miner's new Block
	TaskQueue ->> TaskDistributor: Get Task
	TaskDistributor ->> webAgent: Distribute "SEND_TX" task tp webAgent
	webAgent ->> webAgent: Send New Transaction <br> to Other Clients
```

## Client Structure

Since the client need to get instruction from `webAgent` and `TerminalAgent` at the same time and the `input()` method of Python will clog the main process, we decided to use a multi-process structure to build the client.

There are three main parts of the client:

`Collector` - Collect tasks from outer environment (`webAgent` and `TerminalAgent`)

`Distributor` - Get Task from the Main Task Queue and distribute the task to corresponding worker. `TaskDistributor`

`Worker` - process that do the actual work including mining, transaction verification, new transaction creation etc. (`miner` and `worker`, since miner needs to calculate the hash value for most of the time and we don't want the whole working process being clogged, we put most of the light-calculation work to `worker` while heavy-calculation work to `miner`).

![Structure.png](./Structure.png)

Each worker has its own task queue. The tasks are serialized into the JSON form as example below

```json
{
    "To": "miner",
    "Instruction": "CREATE_BLOCK",
    "args": [
        <Transaction Tx0 ...>,
        <Transaction Tx1 ...>,
        ...
        <Transaction Tx15 ...>,
        currentDifficulty
    ]
}
```