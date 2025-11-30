import subprocess
import re
import os
import sys

PROCESS_COUNTS = [1, 2, 4, 8]
CPP_DIR = "./cpp"
PY_DIR = "./py"

CPP_CMD = ["./run.sh"]
PY_CMD = ["./run.sh"]


def run_and_parse(command, cwd, args):
    full_cmd = command + [str(args)]
    try:
        # Запуск процесса
        res = subprocess.run(
            full_cmd, cwd=cwd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, check=True
        )
        output = res.stdout

        sum_val = re.search(r"Финальная сумма массива: ([0-9.eE+]+)", output)
        time_val = re.search(r"Время выполнения: ([0-9.eE+]+) секунд", output)

        return (
            sum_val.group(1) if sum_val else "Error",
            float(time_val.group(1)) if time_val else 0.0
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {' '.join(full_cmd)}\n{e.stderr}")
        return "Error", 0.0


def main():
    print(f"{'Proc':<5} | {'Lang':<5} | {'Sum Result':<20} | {'Time (sec)':<15}")
    print("-" * 55)

    for n in PROCESS_COUNTS:
        # C++
        sum_cpp, time_cpp = run_and_parse(CPP_CMD, CPP_DIR, n)
        print(f"{n:<5} | {'C++':<5} | {sum_cpp:<20} | {time_cpp:<15.6f}")

        # Python
        sum_py, time_py = run_and_parse(PY_CMD, PY_DIR, n)
        print(f"{n:<5} | {'Py':<5} | {sum_py:<20} | {time_py:<15.6f}")

        print("-" * 55)


if __name__ == "__main__":
    main()
