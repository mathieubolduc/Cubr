using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Camera))]
public class CameraController : MonoBehaviour {

    public GameObject Target;

    public float phi;
    [Range(1f, 179f)]
    public float theta;
    public float distance = 4.0f;

    public float rotateSpeed = 30;
    public float autoRotateSpeed = 30;
    public bool RotateCamera = true;
    private float lastUpdate = 0;
    public float DelayToRotate = 1.0f;
	// Use this for initialization
	void Start () {
    }
	
	// Update is called once per frame
	void Update () {


        if (RotateCamera && (Time.time - lastUpdate)>=DelayToRotate)
        {
            Camera.main.transform.RotateAround(Vector3.zero, Vector3.up, Time.deltaTime * autoRotateSpeed);
        }
        else
        {
            float x = distance * Mathf.Sin(Mathf.Deg2Rad * theta) * Mathf.Cos(Mathf.Deg2Rad * phi);
            float z = distance * Mathf.Sin(Mathf.Deg2Rad * theta) * Mathf.Sin(Mathf.Deg2Rad * phi);
            float y = distance * Mathf.Cos(Mathf.Deg2Rad * theta);

            this.transform.position = new Vector3(x, y, z) + Target.transform.position;
        }

        this.transform.LookAt(Target.transform);

    }

    public void RotateBy(float theta, float phi)
    {


        if (Mathf.Abs(theta) > 0 || Mathf.Abs(phi) > 0)
        {
            if (RotateCamera && (Time.time - lastUpdate) >= DelayToRotate)
            {
                this.theta = Mathf.Rad2Deg * Mathf.Acos((this.transform.position.y - Target.transform.position.y) / this.distance);
                this.phi = Mathf.Rad2Deg * Mathf.Atan((this.transform.position.z - Target.transform.position.z) / (this.transform.position.x - Target.transform.position.x));
            }
            lastUpdate = Time.time;
        }

        this.phi -= phi * rotateSpeed;
        this.theta = Mathf.Clamp(this.theta + theta * rotateSpeed, 10, 170);
    }

    public void ZoomBy(float amt)
    {
        distance += amt;
    }
}
