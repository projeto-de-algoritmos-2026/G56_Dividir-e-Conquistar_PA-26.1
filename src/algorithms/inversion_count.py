"""
Contagem de Inversões — Dividir e Conquistar.

Uma inversão no vetor A é um par (i, j) com i < j e A[i] > A[j].
O total de inversões mede o grau de desordem da sequência.

Complexidade:
  - Força bruta: O(n²)
  - sort_and_count (este módulo): O(n log n)
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class InversionResult:
    sorted_sequence: list[float]
    inversions: int
    max_inversions: int
    percentage: float
    n: int

    def summary(self) -> str:
        return (
            f"n={self.n} | inversões={self.inversions} / {self.max_inversions} "
            f"({self.percentage:.1f}%)"
        )


def merge_and_count(
    arr: list[float],
    temp: list[float],
    left: int,
    mid: int,
    right: int,
) -> int:
    """
    Faz o merge de arr[left..mid] e arr[mid+1..right] (ambos ordenados)
    e conta as inversões cruzadas.

    Inversão cruzada: A[i] > A[j] com i em [left, mid] e j em [mid+1, right].
    Quando arr[i] > arr[j], todos os elementos restantes em arr[left..mid]
    também são > arr[j] (pois a metade esquerda está ordenada), portanto:
        inversões += (mid - i + 1)

    Retorna o número de inversões cruzadas encontradas.
    """
    i = left
    j = mid + 1
    k = left
    inv_count = 0

    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            inv_count += (mid - i + 1)
            j += 1
        k += 1

    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1

    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1

    for idx in range(left, right + 1):
        arr[idx] = temp[idx]

    return inv_count


def sort_and_count(
    arr: list[float],
    temp: list[float],
    left: int,
    right: int,
) -> int:
    """
    Divide e conquista:
    1. Divide arr ao meio (DIVIDIR)
    2. Conta inversões na metade esquerda recursivamente
    3. Conta inversões na metade direita recursivamente
    4. Faz o merge e conta inversões cruzadas (CONQUISTAR)

    Retorna o total de inversões em arr[left..right].
    """
    inv_count = 0

    if left < right:
        mid = (left + right) // 2

        inv_count += sort_and_count(arr, temp, left, mid)
        inv_count += sort_and_count(arr, temp, mid + 1, right)
        inv_count += merge_and_count(arr, temp, left, mid, right)

    return inv_count


def count_inversions(sequence: list[Any]) -> InversionResult:
    """
    Conta inversões na sequência e retorna resultado completo.

    Args:
        sequence: vetor de valores comparáveis (ex: pontuações de dificuldade)

    Returns:
        InversionResult com sorted_sequence, inversions, max_inversions, percentage
    """
    n = len(sequence)

    if n <= 1:
        return InversionResult(
            sorted_sequence=list(sequence),
            inversions=0,
            max_inversions=0,
            percentage=0.0,
            n=n,
        )

    arr = [float(x) for x in sequence]
    temp = arr.copy()

    total = sort_and_count(arr, temp, 0, n - 1)

    max_inv = n * (n - 1) // 2
    percentage = (total / max_inv * 100) if max_inv > 0 else 0.0

    return InversionResult(
        sorted_sequence=arr,
        inversions=total,
        max_inversions=max_inv,
        percentage=round(percentage, 2),
        n=n,
    )


def brute_force_inversions(sequence: list[Any]) -> int:
    """
    Contagem de inversões por força bruta — O(n²).
    Usado apenas para validação do algoritmo eficiente.
    """
    arr = list(sequence)
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def sliding_window_inversions(
    sequence: list[float],
    window_size: int,
) -> list[dict]:
    """
    Calcula inversões em janelas deslizantes da sequência.
    Útil para identificar períodos mais irregulares do calendário.
    """
    results = []
    n = len(sequence)

    for start in range(0, n - window_size + 1):
        window = sequence[start : start + window_size]
        result = count_inversions(window)
        results.append(
            {
                "start_idx": start,
                "end_idx": start + window_size - 1,
                "inversions": result.inversions,
                "max_inversions": result.max_inversions,
                "percentage": result.percentage,
            }
        )

    return results
