// MergeTreeInserter is used with EventSimulator to INSERT new part according to given `inserter` schedule
export class MergeTreeInserter
{
    constructor(sim, mt, inserter)
    {
        this.sim = sim; // EventSimulator
        this.mt = mt; // MergeTree
        this.inserter = inserter;
        this.#iterateInserter();
    }

    #iterateInserter()
    {
        while (true)
        {
            const { value, done } = this.inserter.next();
            if (done)
                return; // No more inserts
            switch (value.type)
            {
                case 'insert':
                    this.mt.insertPart(value.bytes);
                    break;
                case 'sleep':
                    if (value.delay > 0)
                    {
                        this.sim.scheduleAt(this.sim.time + value.delay, "InserterSleep", () => this.#iterateInserter());
                        return;
                    }
                    break;
                default:
                    throw { message: "Unknown merge tree inserter yield type", value};
            }
        }
    }
}
