import React from 'react'
import './Title.css';

function Title() {
  return (
    <nav className="nav">
      <a href="./Home" className='site-title'>Preisjäger</a>
        <ul>
           <li>
            <a href="./Home">Alle</a>
            </li>
            <li>
            <a href="./Mainboards">Mainboards</a>
            </li>
            <li>
            <a href="./Prozessoren">Prozessoren</a>
            </li>
            <li>
            <a href="./Grafikkarten">Grafikkarten</a>
            </li>
        </ul>
    </nav>

  )
}
export default Title