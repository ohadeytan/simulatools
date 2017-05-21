import simulatools
import pprint

def main():
    results = { simulatools.Trace.multi1.typical_caches()[i-1] :
                simulatools.single_run('lru', 'multi1', i)
                for i in range(1,1+8)
              }
    pprint.pprint(results)

if __name__ == "__main__":
    main()

