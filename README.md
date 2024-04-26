# Senior_Design
# Simultaneous Localization and Mapping for Underwater Robots

<img width="712" alt="Screenshot 2024-04-25 at 17 49 24" src="https://github.com/peterguzw0927/Senior_Design/assets/114111503/d67548ab-cd21-4a5e-8454-422b680df239">

# Quick start info
## Initial_2D_SLAM approach
The initial_2D_SLAM folder houses our foundational 2D SLAM (Simultaneous Localization and Mapping) algorithm. This approach sets up a basic 2D meshgrid world populated with a simulated Unmanned Underwater Vehicle (UUV) and landmarks. It's designed to be straightforward to configure and utilize, making it an ideal starting point for those new to SLAM algorithms.

## HoloOcean Scripts
In the HoloOcean scripts folder, you'll find the necessary code to interface with and leverage the HoloOcean underwater simulator. This simulator empowers users to configure customized simulated underwater environments and generate simulated data such as sonar images. By utilizing these scripts, researchers and developers can seamlessly integrate simulated underwater scenarios into their SLAM algorithms, facilitating testing and validation in diverse underwater conditions.

## Bruce SLAM Implementation
Contained within the bruce_slam implementation folder is our implementation of the Bruce SLAM algorithm, packaged neatly into a .vm file format. Bruce SLAM is a sonar-based SLAM algorithm renowned for its robustness and efficiency. Our implementation aims to streamline the usage process, requiring no additional dependencies and offering ease of integration into existing projects. Whether you're conducting research or developing applications in underwater robotics, this implementation provides a powerful tool for underwater mapping and navigation tasks.

## Sonar SLAM Algorithm
The sonar_SLAM folder hosts our proprietary SLAM algorithm tailored specifically for sonar data processing. This algorithm takes in data from Inertial Navigation Systems (INS) and dead reckoning, subsequently processing it through edge detection, landmark detection, and ultimately, SLAM. By leveraging these techniques, our algorithm enables accurate and reliable mapping and localization in underwater environments, even in challenging conditions where traditional sensor data may be limited or noisy. Whether you're exploring marine ecosystems or conducting underwater inspections, our sonar SLAM algorithm offers a versatile solution for underwater mapping and navigation challenges.

# Background & Motivation
Sonar surveys of the seabed are essential to many offshore activities, such as offshore wind farm construction and subsea cable inspection. Uncrewed underwater vehicles (UUVs) provide a lower cost means of gathering this data, but underwater localization is a significant challenge. Without precise localization, survey data gathered by an underwater vehicle is far less useful.  Precise subsea navigation is a significant technical challenge because ubiquitous position reference signals, such as GPS, are unavailable for localization. The state of practice is to use acoustic beacon localization, but the accuracy is limited by the accuracy to which the beacon itself can be placed. Moreover, the beacons are often left in the ocean, littering the seafloor. A potential solution is to use the survey data itself to improve localization. Simultaneous localization and mapping (SLAM) provide techniques for correlating multiple sightings of landmarks in data and using those sightings to correct the estimated position of the vehicle. This corrected localization can then be used to warp the recorded data to better align with its true location. 

Many SLAM algorithms exist in the literature and are available as open-source software packages, each with its advantages and disadvantages.  This capstone project would involve:
- Requirements analysis. What are the features of a SLAM algorithm required for this problem?
- Algorithm tailoring. SLAM algorithms rely on “landmarks” in the data, but the definition and classification of some part of the data as a landmark is problem specific.
- Prototype implementation. Develop or modify open-source candidate solutions for testing.
- Evaluation. Using real world data, use the prototypes to “re-navigate” the vehicle trajectory and produce the best estimate of landmark location.

Draper engineers have previous experience working with several promising SLAM algorithms for vehicle localization applications.  The offline SLAM technique GraphSLAM could potentially work well here, and a project that focused on tailoring this technique to an underwater problem would be acceptable.  A wider-ranging exploration and performance comparison of SLAM algorithms that resulted in a less mature prototype would also be extremely useful.

Draper has access to the deep ocean dataset captured during the search for Air France Flight 447, and we expect to gain access to a US Navy dataset from surveys of Narragansett Bay. These datasets come from different side-scan sonar systems, have different swath widths, and cover very different ocean bottom types. There is also potential to perform limited surveys in the bay as directed by the students for validation of algorithms. A colleague at Woods Hole Oceanographic Institute (WHOI), Jeff Kaeli, has kindly agreed to give a tour of WHOI to the students, which would let the group see operational underwater vehicles, talk to sonar operators, and get a full color picture of what UUV operations look like.

# Expected Deliverables

There is a significant software development and integration component to this project, but also a statistical component (quantifying goodness of fit), and a creative research aspect in landmark definition. 

The main deliverable would be:
Prototype SLAM software
Final report detailing the selected SLAM algorithm
Analysis supporting the algorithm, in particular how the algorithm performs on real data

# Intellectual Property

As for intellectual property issues, the datasets are not open and should not be shared. Pending a decision from legal, the final report would likely be Draper proprietary.  There is no objection to the software prototype developed under the clinic being released as open source.

# Future to do list
If time permits, we plan to extensively test our SLAM algorithm in diverse real-world scenarios and compare its performance with established solutions like Blue-ROV SLAM. Through comprehensive evaluations, we aim to identify strengths and weaknesses, informing further optimization efforts to improve the system's reliability and effectiveness.

