// Scroll Animation
function handleScrollAnimation() {
  const cards = document.querySelectorAll(".card");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const delay = entry.target.getAttribute("data-delay");
          setTimeout(() => {
            entry.target.classList.add("scroll-animate");
          }, parseInt(delay));
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.1,
    }
  );

  cards.forEach((card) => observer.observe(card));
}

// Smooth scroll to resources section
document.querySelector(".scroll-indicator").addEventListener("click", () => {
  document.querySelector(".resources-section").scrollIntoView({
    behavior: "smooth",
  });
});

// Fetch and display news
fetch("http://127.0.0.1:5000/api/news")
  .then((response) => response.json())
  .then((data) => {
    const newsList = document.getElementById("news-list");
    newsList.innerHTML = data.headlines
      .slice(0, 5)
      .map(
        (headline) => `
              <li>
                  <i class="fas fa-newspaper"></i>
                  ${headline}
              </li>
          `
      )
      .join("");
  })
  .catch((error) => console.error("Error fetching news:", error));

// Fetch and display counselors
fetch("http://127.0.0.1:5000/api/counselors")
  .then((response) => response.json())
  .then((data) => {
    const counselorsList = document.getElementById("counselors-list");
    counselorsList.innerHTML = data.counselors
      .map(
        (counselor) => `
              <li>
                  <i class="fas fa-user-md"></i>
                  <strong>${counselor.name}</strong>
                  <p>${counselor.location}</p>
                  <p><i class="fas fa-phone"></i> ${counselor.contact}</p>
              </li>
          `
      )
      .join("");
  })
  .catch((error) => console.error("Error fetching counselors:", error));

// Fetch and display exercises
fetch("http://127.0.0.1:5000/api/cbt-exercises")
  .then((response) => response.json())
  .then((data) => {
    const exercisesList = document.getElementById("exercises-list");
    exercisesList.innerHTML = data.exercises
      .map(
        (exercise) => `
              <li>
                  <i class="fas fa-brain"></i>
                  <strong>${exercise.name}</strong>
                  <p>${exercise.description}</p>
                  <p><i class="fas fa-clock"></i> ${exercise.recommended_duration}</p>
              </li>
          `
      )
      .join("");
  })
  .catch((error) => console.error("Error fetching exercises:", error));

// Initialize scroll animations
document.addEventListener("DOMContentLoaded", () => {
  handleScrollAnimation();
});
