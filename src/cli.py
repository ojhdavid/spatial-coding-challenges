import argparse
from .selector import choose_random_problem
from ai.gpt_client import generate_spatial_coding_problem

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['local','gpt'], default='local')
    parser.add_argument('--difficulty', type=int, default=1)
    parser.add_argument('--topic', type=str, default=None)
    parser.add_argument('--context', type=str, default='')
    args = parser.parse_args()

    if args.mode == 'local':
        p = choose_random_problem(args.difficulty, args.topic)
        if not p:
            print('No matching problem found.')
            return
        print(f"[{p['id']}] {p['title']}\n")
        print(p['description'])
    else:
        text = generate_spatial_coding_problem(args.difficulty, args.topic or 'scanpy', args.context)
        print(text)

if __name__ == '__main__':
    main()
