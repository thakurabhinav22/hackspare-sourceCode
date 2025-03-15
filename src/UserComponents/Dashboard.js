import React, { useEffect, useState } from "react";
import { ref, get } from "firebase/database";
import Cookies from "js-cookie";
import { database } from "../Admin/firebase";
import { useNavigate } from "react-router-dom"; 
import Sidebar from "../UserComponents/Sidebar";
import "./Dashboard.css";
import Swal from "sweetalert2";
import DashboardContent from "./DashboardContent";

function Dashboard() {
  const [userName, setUserName] = useState("");
  const [Surname, setSurName] = useState("");
  const [userBranch, setBranch] = useState("");
  
  const navigate = useNavigate(); 

 
  const showAlertMessage = (message, type) => {
    Swal.fire({
      title: message,
      icon: type,
      position: 'top',
      toast: true,
      showConfirmButton: false,
      timer: 5000,
      timerProgressBar: true,
    });
  };

  useEffect(() => {
    document.title = "TheLearnMax - Dashboard";
    const userId = Cookies.get("userSessionCred");
    if (!userId) {
    
      showAlertMessage("No user session found. Please log in again.", "warning");
      navigate("/"); 
      return; 
    }

    // Reference to the user's data in Firebase
    const userRef = ref(database, `user/${userId}`);

    // Fetch user data from Firebase
    get(userRef)
      .then((snapshot) => {
        if (snapshot.exists()) {
          const userData = snapshot.val();
          if (userData && userData.Name) {
            setUserName(userData.Name);
            setSurName(userData.Surname);
            setBranch(userData.Branch);
          } else {
            console.log("User data does not contain a Name field.");
            showAlertMessage("No user data found in Firebase.", "error");
            Cookies.remove("userSessionCred"); // Clear the cookie
            navigate("/"); // Redirect to the login page
          }
        } else {
          console.log("No user data found in Firebase.");
          showAlertMessage("No user found in Firebase.", "error");
          Cookies.remove("userSessionCred"); // Clear the cookie
          navigate("/"); // Redirect to the login page
        }
      })
      .catch((error) => {
        console.error("Error fetching user data from Firebase:", error);
        showAlertMessage("Error fetching user data. Please try again later.", "error");
        Cookies.remove("userSessionCred"); // Clear the cookie
        navigate("/"); // Redirect to the login page
      });
  }, [navigate]); // Add navigate to dependency array

  return (
    <div className="dashboard-container">
      {/* Pass userName, SurName, and Branch as props */}
      <Sidebar userName={userName} SurName={Surname} Branch={userBranch} />
      <DashboardContent/>
    </div>
  );
}

export default Dashboard;
