using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class RubiksCubePrefab : MonoBehaviour {

    public GameObject CubePrefab;

    public RubiksCube RC;//the actual rubiks cube data structure
    public List<List<List<GameObject>>> cubePrefabMatrix;
    public float spacing = 1.05f;
    public float rotationSpeed = 40;
    public bool Animating = false;
    // Use this for initialization
    public void Start () {

    }

    public void InitializePrefabs()
    {
        cubePrefabMatrix = new List<List<List<GameObject>>>();
        for (int x = 0; x < 3; x++)
        {
            List<List<GameObject>> PrefabRow = new List<List<GameObject>>();
            for (int y = 0; y < 3; y++)
            {
                List<GameObject> PrefabColumn = new List<GameObject>();
                for (int z = 0; z < 3; z++)
                {
                    GameObject cubePrefab = Instantiate(CubePrefab, Vector3.zero, Quaternion.identity) as GameObject;
                    cubePrefab.name = "Cube " + new Vector3(x, y, z);
                    cubePrefab.transform.SetParent(transform);
                    cubePrefab.transform.position = new Vector3((x - 1), (y - 1), (z - 1)) * spacing;
                    //cubePrefab.GetComponent<CubePrefab>().refreshPanels(RC.cubeMatrix[x][y][z]);
                    PrefabColumn.Add(cubePrefab);
                }
                PrefabRow.Add(PrefabColumn);
            }
            cubePrefabMatrix.Add(PrefabRow);
        }
    }

    public void InitializeAll()
    {
        if(cubePrefabMatrix!=null)
        {
            cubePrefabMatrix.Clear();
            foreach(Transform child in this.GetComponentInChildren<Transform>())
            {
                Destroy(child.gameObject);
            }
        }

        RC = new RubiksCube();
        InitializePrefabs();
        RefreshPanels();
    }

    public void ResetView()
    {
        RC = new RubiksCube();
        resetCubePrefabPositions();
        RefreshPanels();
    }

    void Update()
    {
        //RefreshPanels();
    }

    public void resetCubePrefabPositions()
    {
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                for (int k = 0; k < 3; k++)
                {
                    cubePrefabMatrix[i][j][k].transform.position = new Vector3((i - 1), (j - 1), (k - 1)) * spacing;
                    cubePrefabMatrix[i][j][k].transform.rotation = Quaternion.identity;
                }
            }
        }
    }
    
    public IEnumerator animateCustomSequence(string seq)
    {
        Animating = true;
        int step = 0;


        while (step < seq.Length)
        {
            char c = seq[step];//get the character of the turn to run
            bool clockwise = true;
            if (step + 1 < seq.Length)
            {
                if (seq[step + 1] == 'i')//does the next character indicate an inverse operation?
                {
                    clockwise = false;
                    step++;//increment past inverse character
                }
            }
            //===========================

            float totalRotation = 0;
            int dir = 1;
            if (clockwise)
                dir = -1;
            float delta = 0;

            if (c == 'R'){
                RC.rotateRightFace(clockwise);
                while (Mathf.Abs(totalRotation) < 90){
                    delta = -1* dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    for (int i = 0; i < 3; i++) { for (int j = 0; j < 3; j++) { cubePrefabMatrix[2][i][j].transform.RotateAround(transform.position, transform.right, delta); } }
                    yield return null;
                }
            }
            else if (c == 'L')
            {
                RC.rotateLeftFace(clockwise);
                while (Mathf.Abs(totalRotation) < 90)
                {
                    delta = dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    for (int i = 0; i < 3; i++) { for (int j = 0; j < 3; j++) { cubePrefabMatrix[0][i][j].transform.RotateAround(transform.position, transform.right, delta); } }
                    yield return null;
                }
            }
            else if (c == 'U')
            {
                RC.rotateTopFace(clockwise);
                while (Mathf.Abs(totalRotation) < 90)
                {
                    delta = -1 * dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    for (int i = 0; i < 3; i++) { for (int j = 0; j < 3; j++) { cubePrefabMatrix[i][2][j].transform.RotateAround(transform.position, transform.up, delta); } }
                    yield return null;
                }
            }
            else if (c == 'D')
            {
                RC.rotateBottomFace(clockwise);
                while (Mathf.Abs(totalRotation) < 90)
                {
                    delta = dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    for (int i = 0; i < 3; i++) { for (int j = 0; j < 3; j++) { cubePrefabMatrix[i][0][j].transform.RotateAround(transform.position, transform.up, delta); } }
                    yield return null;
                }
            }
            else if (c == 'F')
            {
                RC.rotateFrontFace(clockwise);
                while (Mathf.Abs(totalRotation) < 90)
                {
                    delta = dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    for (int i = 0; i < 3; i++) { for (int j = 0; j < 3; j++) { cubePrefabMatrix[i][j][0].transform.RotateAround(transform.position, transform.forward, delta); } }
                    yield return null;
                }
            }
            else if (c == 'B')
            {
                RC.rotateBackFace(clockwise);
                while (Mathf.Abs(totalRotation) < 90)
                {
                    delta = -1 * dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    for (int i = 0; i < 3; i++) { for (int j = 0; j < 3; j++) { cubePrefabMatrix[i][j][2].transform.RotateAround(transform.position, transform.forward, delta); } }
                    yield return null;
                }
            }
            else if (c == 'X')
            {
                RC.turnCubeX(clockwise);
                while (Mathf.Abs(totalRotation) < 90)
                {
                    delta = dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    transform.RotateAround(transform.position, transform.right, delta);
                    yield return null;
                }
            }
            else if (c == 'Y')
            {
                RC.turnCubeY(clockwise);
                while (Mathf.Abs(totalRotation) < 90)
                {
                    delta = dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    transform.RotateAround(transform.position, transform.up, delta);
                    yield return null;
                }
            }
            else if (c == 'Z')
            {
                RC.turnCubeZ(clockwise);
                while (Mathf.Abs(totalRotation) < 90)
                {
                    delta = dir * rotationSpeed * Time.deltaTime;
                    totalRotation += delta;
                    transform.RotateAround(transform.position, transform.forward, delta);
                    yield return null;
                }
            }


            step++;
            transform.rotation = Quaternion.identity;
            transform.position = Vector3.zero;
            resetCubePrefabPositions();
            RefreshPanels();
        }
        this.Animating = false;
        yield return null;
    }

    public void RefreshPanels()
    {
        for (int x = 0; x < 3; x++)
        {
            for (int y = 0; y < 3; y++)
            {
                for (int z = 0; z < 3; z++)
                {
                    cubePrefabMatrix[x][y][z].GetComponent<CubePrefab>().refreshPanels(RC.cubeMatrix[x][y][z]);
                }
            }
        }
    }


}
