import React from 'react'
import ImageDropBox from './ImageDropdown'
import ParticlesComponent from './ParticlesComponent'
import { Container } from 'postcss'
import ParticlesContainer from './ParticlesContainer'
import { FileUpload } from './ui/FileUpload'
import { WavyBackground } from './ui/wavyBg'

const Home = () => {
  return (
    <>
      <div id='home' className='w-full bg-black '>
      <WavyBackground className="max-w-4xl mx-auto py-40">
      <p className="text-4xl md:text-6xl lg:text-8xl font-sora font-bold tracking-tighter text-slate-50">
            Explore the RAMIT of AI with Artifacta
      </p>
      <p className="text-lg md:text-2xl lg:text-3xl font-sora font-bold text-slate-100 mt-4 md:mt-8">
            Unleash the Power of AI with Artifacta. Artifacta leverages AI to help you from gathering the missing words of a manuscript to getting a totally restored 3D model of your provided image.
      </p>
      </WavyBackground>
          {/* ImageDropBox Component */}
          <div className='py-10 px-96 md:auto'>
            <FileUpload className="bg-black"></FileUpload>
          </div>
        </div>
    </>
  );
}

export default Home;

