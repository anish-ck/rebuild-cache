export class LRUCache<K, V> {
  private cache: Map<K, V>;
  private readonly maxSize: number;
  private _hits: number = 0;
  private _misses: number = 0;
  private _evictions: number = 0;

  constructor(maxSize: number = 40) {
    this.cache = new Map();
    this.maxSize = maxSize;
  }

  get(key: K): V | undefined {
    if (!this.cache.has(key)) {
      this._misses++;
      return undefined;
    }
    this._hits++;
    // Move to end (most recently used)
    const value = this.cache.get(key)!;
    this.cache.delete(key);
    this.cache.set(key, value);
    return value;
  }

  set(key: K, value: V): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.maxSize) {
      // Evict LRU (first entry)
      const firstKey = this.cache.keys().next().value;
      if (firstKey !== undefined) {
        this.cache.delete(firstKey);
        this._evictions++;
      }
    }
    this.cache.set(key, value);
  }

  has(key: K): boolean {
    return this.cache.has(key);
  }

  delete(key: K): boolean {
    return this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
    this._hits = 0;
    this._misses = 0;
    this._evictions = 0;
  }

  get size(): number {
    return this.cache.size;
  }

  get hits(): number { return this._hits; }
  get misses(): number { return this._misses; }
  get evictions(): number { return this._evictions; }
  get maxCapacity(): number { return this.maxSize; }

  getStats() {
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      hits: this._hits,
      misses: this._misses,
      evictions: this._evictions,
    };
  }
}
