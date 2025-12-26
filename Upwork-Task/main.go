package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
)

type Candidate struct {
	id         int
	mutual     int
	friendCnt  int
}

func main() {
	in := bufio.NewReader(os.Stdin)

	var N, M, K, L int
	fmt.Fscan(in, &N, &M, &K, &L)

	// Adjacency list
	friends := make([]map[int]bool, N+1)
	for i := 1; i <= N; i++ {
		friends[i] = make(map[int]bool)
	}

	// Read friendships (undirected)
	for i := 0; i < M; i++ {
		var x, y int
		fmt.Fscan(in, &x, &y)
		friends[x][y] = true
		friends[y][x] = true
	}

	// Degree (total friend count)
	degree := make([]int, N+1)
	for i := 1; i <= N; i++ {
		degree[i] = len(friends[i])
	}

	isFriendOfK := friends[K]

	candidatesWithMutual := make([]Candidate, 0)
	candidatesWithoutMutual := make([]Candidate, 0)

	// Evaluate all non-friends
	for u := 1; u <= N; u++ {
		if u == K || isFriendOfK[u] {
			continue
		}

		// Count mutual friends with K
		mutual := 0
		for f := range friends[u] {
			if isFriendOfK[f] {
				mutual++
			}
		}

		c := Candidate{
			id:        u,
			mutual:    mutual,
			friendCnt: degree[u],
		}

		if mutual > 0 {
			candidatesWithMutual = append(candidatesWithMutual, c)
		} else {
			candidatesWithoutMutual = append(candidatesWithoutMutual, c)
		}
	}

	// Sort candidates with mutual friends
	sort.Slice(candidatesWithMutual, func(i, j int) bool {
		if candidatesWithMutual[i].mutual != candidatesWithMutual[j].mutual {
			return candidatesWithMutual[i].mutual > candidatesWithMutual[j].mutual
		}
		if candidatesWithMutual[i].friendCnt != candidatesWithMutual[j].friendCnt {
			return candidatesWithMutual[i].friendCnt > candidatesWithMutual[j].friendCnt
		}
		return candidatesWithMutual[i].id < candidatesWithMutual[j].id
	})

	// Sort candidates without mutual friends (only by activity then ID)
	sort.Slice(candidatesWithoutMutual, func(i, j int) bool {
		if candidatesWithoutMutual[i].friendCnt != candidatesWithoutMutual[j].friendCnt {
			return candidatesWithoutMutual[i].friendCnt > candidatesWithoutMutual[j].friendCnt
		}
		return candidatesWithoutMutual[i].id < candidatesWithoutMutual[j].id
	})

	// Build result
	result := make([]int, 0, L)

	for _, c := range candidatesWithMutual {
		if len(result) == L {
			break
		}
		result = append(result, c.id)
	}

	for _, c := range candidatesWithoutMutual {
		if len(result) == L {
			break
		}
		result = append(result, c.id)
	}

	// Fill remaining with 0 if needed
	for len(result) < L {
		result = append(result, 0)
	}

	// Output
	out := bufio.NewWriter(os.Stdout)
	for i := 0; i < len(result); i++ {
		if i > 0 {
			fmt.Fprint(out, " ")
		}
		fmt.Fprint(out, result[i])
	}
	out.Flush()
}
